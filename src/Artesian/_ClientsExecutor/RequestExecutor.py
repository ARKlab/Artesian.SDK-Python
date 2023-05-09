# type: ignore
# flake8: noqa

import asyncio
import random
import six
import sys
import time
import traceback

from Artesian.Exceptions import ArtesianSdkRequestException, ArtesianSdkServerException


# sys.maxint / 2, since Python 3.2 doesn't have a sys.maxint...
MAX_WAIT = 1073741823


class _RequestExecutor:
    """
    This class handles all of the requests sent by the Artesian Client.
    """

    def __init__(self, policy) -> None:
        self.__policy = policy
        self.__sem = None

    def getSemaphore(self):
        if self.__sem is None:
            self.__sem = asyncio.Semaphore(self.__policy.maxParallelism)
        return self.__sem

    async def __do(self, callback, *args, **kwargs):
        async with self.getSemaphore():
            return await callback(*args, **kwargs)

    async def exec(self, callback, *args, **kwargs):
        r = Retrying(
            wait_fixed=self.__policy.retryWaitTime,
            stop_max_attempt_number=self.__policy.maxRetry,
            retry_on_exception=lambda e: isinstance(e, ArtesianSdkServerException)
            or isinstance(e, ArtesianSdkRequestException),
        )
        return await r.call(self.__do, callback, *args, **kwargs)


class Retrying(object):
    def __init__(
        self,
        stop=None,
        wait=None,
        stop_max_attempt_number=None,
        stop_max_delay=None,
        wait_fixed=None,
        wait_random_min=None,
        wait_random_max=None,
        wait_incrementing_start=None,
        wait_incrementing_increment=None,
        wait_incrementing_max=None,
        wait_exponential_multiplier=None,
        wait_exponential_max=None,
        retry_on_exception=None,
        retry_on_result=None,
        wrap_exception=False,
        stop_func=None,
        wait_func=None,
        wait_jitter_max=None,
        before_attempts=None,
        after_attempts=None,
    ) -> None:
        self._stop_max_attempt_number = (
            5 if stop_max_attempt_number is None else stop_max_attempt_number
        )
        self._stop_max_delay = 100 if stop_max_delay is None else stop_max_delay
        self._wait_fixed = 1000 if wait_fixed is None else wait_fixed
        self._wait_random_min = 0 if wait_random_min is None else wait_random_min
        self._wait_random_max = 1000 if wait_random_max is None else wait_random_max
        self._wait_incrementing_start = (
            0 if wait_incrementing_start is None else wait_incrementing_start
        )
        self._wait_incrementing_increment = (
            100 if wait_incrementing_increment is None else wait_incrementing_increment
        )
        self._wait_exponential_multiplier = (
            1 if wait_exponential_multiplier is None else wait_exponential_multiplier
        )
        self._wait_exponential_max = (
            MAX_WAIT if wait_exponential_max is None else wait_exponential_max
        )
        self._wait_incrementing_max = (
            MAX_WAIT if wait_incrementing_max is None else wait_incrementing_max
        )
        self._wait_jitter_max = 0 if wait_jitter_max is None else wait_jitter_max
        self._before_attempts = before_attempts
        self._after_attempts = after_attempts

        # TODO add chaining of stop behaviors
        # stop behavior
        stop_funcs = []
        if stop_max_attempt_number is not None:
            stop_funcs.append(self.stop_after_attempt)

        if stop_max_delay is not None:
            stop_funcs.append(self.stop_after_delay)

        if stop_func is not None:
            self.stop = stop_func

        elif stop is None:
            self.stop = lambda attempts, delay: any(
                f(attempts, delay) for f in stop_funcs
            )

        else:
            self.stop = getattr(self, stop)

        # TODO add chaining of wait behaviors
        # wait behavior
        wait_funcs = []
        if wait_fixed is not None:
            wait_funcs.append(self.fixed_sleep)

        if wait_random_min is not None or wait_random_max is not None:
            wait_funcs.append(self.random_sleep)

        if (
            wait_incrementing_start is not None
            or wait_incrementing_increment is not None
        ):
            wait_funcs.append(self.incrementing_sleep)

        if wait_exponential_multiplier is not None or wait_exponential_max is not None:
            wait_funcs.append(self.exponential_sleep)

        if wait_func is not None:
            self.wait = wait_func

        elif wait is None:
            self.wait = lambda attempts, delay: max(
                f(attempts, delay) for f in wait_funcs
            )

        else:
            self.wait = getattr(self, wait)

        # retry on exception filter
        if retry_on_exception is None:
            self._retry_on_exception = self.always_reject
        else:
            self._retry_on_exception = retry_on_exception

        # retry on result filter
        if retry_on_result is None:
            self._retry_on_result = self.never_reject
        else:
            self._retry_on_result = retry_on_result

        self._wrap_exception = wrap_exception

    def stop_after_attempt(self, previous_attempt_number, delay_since_first_attempt_ms):
        """Stop after the previous attempt >= stop_max_attempt_number."""
        return previous_attempt_number >= self._stop_max_attempt_number

    def stop_after_delay(self, previous_attempt_number, delay_since_first_attempt_ms):
        """Stop after the time from the first attempt >= stop_max_delay."""
        return delay_since_first_attempt_ms >= self._stop_max_delay

    @staticmethod
    def no_sleep(previous_attempt_number, delay_since_first_attempt_ms):
        """Don't sleep at all before retrying."""
        return 0

    def fixed_sleep(
        self, previous_attempt_number: int, delay_since_first_attempt_ms: int
    ) -> int:
        """Sleep a fixed amount of time between each retry."""
        return self._wait_fixed

    def random_sleep(
        self, previous_attempt_number: int, delay_since_first_attempt_ms: int
    ) -> int:
        """Sleep a random amount of time between wait_random_min and wait_random_max"""
        return random.randint(self._wait_random_min, self._wait_random_max)

    def incrementing_sleep(
        self, previous_attempt_number: int, delay_since_first_attempt_ms: int
    ) -> int:
        """
        Sleep an incremental amount of time after each attempt, starting at
        wait_incrementing_start and incrementing by wait_incrementing_increment
        """
        result = self._wait_incrementing_start + (
            self._wait_incrementing_increment * (previous_attempt_number - 1)
        )
        if result > self._wait_incrementing_max:
            result = self._wait_incrementing_max
        if result < 0:
            result = 0
        return result

    def exponential_sleep(
        self, previous_attempt_number: int, delay_since_first_attempt_ms: int
    ) -> int:
        exp = 2**previous_attempt_number
        result = self._wait_exponential_multiplier * exp
        if result > self._wait_exponential_max:
            result = self._wait_exponential_max
        if result < 0:
            result = 0
        return result

    @staticmethod
    def never_reject(result):
        return False

    @staticmethod
    def always_reject(result):
        return True

    def should_reject(self, attempt):
        reject = False
        if attempt.has_exception:
            reject |= self._retry_on_exception(attempt.value[1])
        else:
            reject |= self._retry_on_result(attempt.value)

        return reject

    async def call(self, fn, *args, **kwargs):
        start_time = int(round(time.time() * 1000))
        attempt_number = 1
        while True:
            if self._before_attempts:
                self._before_attempts(attempt_number)
            try:
                res = await fn(*args, **kwargs)
                attempt = Attempt(res, attempt_number, False)
            except:
                tb = sys.exc_info()
                attempt = Attempt(tb, attempt_number, True)

            if not self.should_reject(attempt):
                return attempt.get(self._wrap_exception)

            if self._after_attempts:
                self._after_attempts(attempt_number)

            delay_since_first_attempt_ms = int(round(time.time() * 1000)) - start_time
            if self.stop(attempt_number, delay_since_first_attempt_ms):
                if not self._wrap_exception and attempt.has_exception:
                    # get() on an attempt with an exception should cause it to be
                    # raised, but raise just in case
                    attempt.get()
                else:
                    raise RetryError(attempt)
            else:
                sleep = self.wait(attempt_number, delay_since_first_attempt_ms)
                if self._wait_jitter_max:
                    jitter = random.random() * self._wait_jitter_max
                    sleep = sleep + max(0, jitter)
                await asyncio.sleep(sleep / 1000.0)

            attempt_number += 1


class Attempt(object):
    """
    An Attempt encapsulates a call to a target function that may end as a
    normal return value from the function or an Exception depending on what
    occurred during the execution.
    """

    def __init__(self, value, attempt_number, has_exception) -> None:
        self.value = value
        self.attempt_number = attempt_number
        self.has_exception = has_exception

    def get(self, wrap_exception=False):
        """
        Return the return value of this Attempt instance or raise an Exception.
        If wrap_exception is true, this Attempt is wrapped inside of a
        RetryError before being raised.
        """
        if self.has_exception:
            if wrap_exception:
                raise RetryError(self)
            else:
                six.reraise(self.value[0], self.value[1], self.value[2])
        else:
            return self.value

    def __repr__(self):
        if self.has_exception:
            return "Attempts: {0}, Error:\n{1}".format(
                self.attempt_number, "".join(traceback.format_tb(self.value[2]))
            )
        else:
            return "Attempts: {0}, Value: {1}".format(self.attempt_number, self.value)


class RetryError(Exception):
    """
    A RetryError encapsulates the last Attempt instance right before giving up.
    """

    def __init__(self, last_attempt) -> None:
        self.last_attempt = last_attempt

    def __str__(self):
        return "RetryError[{0}]".format(self.last_attempt)
