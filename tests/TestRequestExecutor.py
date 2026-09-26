import asyncio
import traceback
import unittest
from unittest.mock import AsyncMock, call, patch

from Artesian.ArtesianPolicyConfig import ArtesianPolicyConfig
from Artesian.Exceptions import ArtesianSdkServerException
from Artesian._ClientsExecutor.RequestExecutor import Attempt, RetryError, Retrying, _RequestExecutor


class TestRequestExecutor(unittest.IsolatedAsyncioTestCase):
    async def test_callback_forwarding_result_identity_and_semaphore_reuse(self) -> None:
        executor = _RequestExecutor(ArtesianPolicyConfig(maxParallelism=1))
        semaphore = executor.getSemaphore()
        result = object()

        async def callback(value: object, /, *, label: str) -> object:
            self.assertTrue(semaphore.locked())
            self.assertEqual(label, "forwarded")
            return value

        self.assertIs(await executor.exec(callback, result, label="forwarded"), result)
        self.assertIs(executor.getSemaphore(), semaphore)
        self.assertFalse(semaphore.locked())

    async def test_sdk_exception_retries_and_exhaustion_preserve_identity(self) -> None:
        executor = _RequestExecutor(ArtesianPolicyConfig(maxRetry=3, retryWaitTime=25))
        error = ArtesianSdkServerException("GET", "https://example.invalid", 503)
        attempts = 0

        async def callback() -> None:
            nonlocal attempts
            attempts += 1
            raise error

        with patch("Artesian._ClientsExecutor.RequestExecutor.asyncio.sleep", new_callable=AsyncMock) as sleep:
            with self.assertRaises(ArtesianSdkServerException) as caught:
                await executor.exec(callback)

        self.assertIs(caught.exception, error)
        self.assertEqual(attempts, 3)
        self.assertEqual(sleep.await_args_list, [call(0.025), call(0.025)])
        self.assertFalse(executor.getSemaphore().locked())

    async def test_non_retryable_exception_and_cancellation_preserve_traceback(self) -> None:
        for error in (RuntimeError("failure"), asyncio.CancelledError("cancelled")):
            with self.subTest(exception=type(error)):
                executor = _RequestExecutor(ArtesianPolicyConfig(maxRetry=3, maxParallelism=1))
                attempts = 0

                async def callback(error: RuntimeError | asyncio.CancelledError = error) -> None:
                    nonlocal attempts
                    attempts += 1
                    raise error

                try:
                    await executor.exec(callback)
                except (RuntimeError, asyncio.CancelledError) as caught:
                    self.assertIs(caught, error)
                    self.assertEqual(traceback.extract_tb(caught.__traceback__)[-1].name, "callback")
                else:
                    self.fail("The callback exception was not propagated")

                self.assertEqual(attempts, 1)
                self.assertFalse(executor.getSemaphore().locked())

    async def test_result_retries_callable_overrides_and_hooks(self) -> None:
        before: list[int] = []
        after: list[int] = []
        stops: list[tuple[int, int]] = []
        waits: list[tuple[int, int]] = []
        results = iter((0, 0, 1))

        def stop(attempt: int, delay: int) -> bool:
            stops.append((attempt, delay))
            return attempt >= 3

        def wait(attempt: int, delay: int) -> float:
            waits.append((attempt, delay))
            return 7.5

        async def callback() -> int:
            return next(results)

        retry: Retrying[int] = Retrying(
            stop="unused_when_overridden",
            wait="unused_when_overridden",
            retry_on_result=lambda result: result == 0,
            stop_func=stop,
            wait_func=wait,
            before_attempts=before.append,
            after_attempts=after.append,
        )
        with (
            patch("Artesian._ClientsExecutor.RequestExecutor.time.time", side_effect=[1, 1.01, 1.02]),
            patch("Artesian._ClientsExecutor.RequestExecutor.asyncio.sleep", new_callable=AsyncMock) as sleep,
        ):
            self.assertEqual(await retry.call(callback), 1)

        self.assertEqual(before, [1, 2, 3])
        self.assertEqual(after, [1, 2])
        self.assertEqual(stops, [(1, 10), (2, 20)])
        self.assertEqual(waits, stops)
        self.assertEqual(sleep.await_args_list, [call(0.0075), call(0.0075)])

    async def test_named_methods_and_rejected_exception_shaped_result(self) -> None:
        result = (ValueError, ValueError("ordinary result"), None)

        async def callback() -> tuple[type[ValueError], ValueError, None]:
            return result

        retry: Retrying[tuple[type[ValueError], ValueError, None]] = Retrying(
            stop="stop_after_attempt",
            wait="no_sleep",
            stop_max_attempt_number=2,
            retry_on_result=lambda value: value is result,
        )
        with patch("Artesian._ClientsExecutor.RequestExecutor.asyncio.sleep", new_callable=AsyncMock) as sleep:
            with self.assertRaises(RetryError) as caught:
                await retry.call(callback)

        attempt = caught.exception.last_attempt
        self.assertEqual(attempt.attempt_number, 2)
        self.assertFalse(attempt.has_exception)
        self.assertIs(attempt.get(), result)
        self.assertEqual(str(caught.exception), f"RetryError[{attempt!r}]")
        sleep.assert_awaited_once_with(0)

    async def test_wrapped_exception_retains_original_exception_and_traceback(self) -> None:
        error = ValueError("wrapped")

        async def callback() -> None:
            raise error

        for reject in (False, True):
            with self.subTest(retry=reject):
                retry: Retrying[None] = Retrying(
                    stop_max_attempt_number=1,
                    retry_on_exception=lambda exception, reject=reject: reject,
                    wrap_exception=True,
                )
                with self.assertRaises(RetryError) as caught:
                    await retry.call(callback)

                attempt = caught.exception.last_attempt
                self.assertTrue(attempt.has_exception)
                self.assertEqual(attempt.attempt_number, 1)
                self.assertIn("callback", repr(attempt))
                with self.assertRaises(ValueError) as unwrapped:
                    attempt.get()
                self.assertIs(unwrapped.exception, error)

    async def test_default_retry_predicate_still_retries_cancellation(self) -> None:
        error = asyncio.CancelledError("retry this callback cancellation")
        attempts = 0

        async def callback() -> str:
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise error
            return "success"

        retry: Retrying[str] = Retrying(stop_max_attempt_number=3, wait_fixed=0)
        with patch("Artesian._ClientsExecutor.RequestExecutor.asyncio.sleep", new_callable=AsyncMock) as sleep:
            self.assertEqual(await retry.call(callback), "success")

        self.assertEqual(attempts, 3)
        self.assertEqual(sleep.await_count, 2)

    async def test_combined_waits_jitter_and_delay_stop(self) -> None:
        retry: Retrying[int] = Retrying(
            stop_max_delay=30,
            wait_fixed=10,
            wait_incrementing_start=5,
            wait_incrementing_increment=10,
            wait_exponential_multiplier=3,
            wait_exponential_max=20,
            wait_jitter_max=4,
            retry_on_result=lambda result: True,
        )

        async def callback() -> int:
            return 0

        with (
            patch("Artesian._ClientsExecutor.RequestExecutor.time.time", side_effect=[1, 1.01, 1.02, 1.03]),
            patch("Artesian._ClientsExecutor.RequestExecutor.random.random", return_value=0.5),
            patch("Artesian._ClientsExecutor.RequestExecutor.asyncio.sleep", new_callable=AsyncMock) as sleep,
        ):
            with self.assertRaises(RetryError) as caught:
                await retry.call(callback)

        self.assertEqual(caught.exception.last_attempt.attempt_number, 3)
        self.assertEqual(sleep.await_args_list, [call(0.012), call(0.017)])

    def test_attempt_and_retry_helper_defaults(self) -> None:
        attempt: Attempt[None] = Attempt(None, 1, False)
        self.assertIsNone(attempt.get())
        self.assertEqual(repr(attempt), "Attempts: 1, Value: None")
        retry: Retrying[object] = Retrying()
        self.assertFalse(retry.stop_after_attempt(4, 0))
        self.assertTrue(retry.stop_after_attempt(5, 0))
        self.assertFalse(retry.stop_after_delay(1, 99))
        self.assertTrue(retry.stop_after_delay(1, 100))
        self.assertEqual(retry.fixed_sleep(1, 0), 1000)
        self.assertEqual(retry.incrementing_sleep(3, 0), 200)
        self.assertEqual(retry.exponential_sleep(3, 0), 8)
        with patch("Artesian._ClientsExecutor.RequestExecutor.random.randint", return_value=42) as randint:
            self.assertEqual(retry.random_sleep(1, 0), 42)
        randint.assert_called_once_with(0, 1000)

        bounded: Retrying[object] = Retrying(
            wait_incrementing_start=-5,
            wait_incrementing_increment=10,
            wait_incrementing_max=7,
            wait_exponential_multiplier=-1,
        )
        self.assertEqual(bounded.incrementing_sleep(1, 0), 0)
        self.assertEqual(bounded.incrementing_sleep(3, 0), 7)
        self.assertEqual(bounded.exponential_sleep(1, 0), 0)
