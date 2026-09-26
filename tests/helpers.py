from __future__ import annotations

from collections.abc import Callable
from typing import Any
from unittest.mock import Mock, patch
from urllib.parse import unquote, urlparse

import Artesian.GMEPublicOffers as _GMEPO
import Artesian.Query._Query as _Query


class Qs:
    def __init__(self: Qs, mock: Mock) -> None:
        self._mock = mock

    def getQs(self: Qs) -> dict[str, str]:
        return dict(
            map(
                lambda x: x.split("="),
                unquote(urlparse(self._mock.call_args.args[0][0]).query).split("&"),
            )
        )

    def getPath(self: Qs) -> str:
        return urlparse(self._mock.call_args.args[0][0]).path


class QsPO:
    def __init__(self: QsPO, mock: Mock) -> None:
        self._mock = mock

    def getQs(self: QsPO) -> dict[str, str]:
        return dict(
            map(
                lambda x: x.split("="),
                unquote(urlparse(self._mock.call_args.args[0]).query).split("&"),
            )
        )

    def getPath(self: QsPO) -> str:
        return urlparse(self._mock.call_args.args[0]).path


def TrackRequests(func: Callable) -> Callable[[Any, Qs], None]:
    @patch.object(_Query._Query, "_exec")
    def wrapper(self: Any, mock: Mock) -> None:
        func(self, Qs(mock))

    return wrapper


def TrackGMEPORequests(func: Callable) -> Callable[[Any, QsPO], None]:
    @patch.object(_GMEPO.GMEPublicOfferQuery, "_exec")
    def wrapper(self: Any, mock: Mock) -> None:
        func(self, QsPO(mock))

    return wrapper
