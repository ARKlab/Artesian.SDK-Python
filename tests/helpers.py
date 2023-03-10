from __future__ import annotations
from ast import Dict
from typing import Any, Callable
from unittest.mock import Mock, patch
import Artesian.Query._Query as _Query
from urllib.parse import urlparse


class Qs:
    def __init__(self: Qs, mock: Mock) -> None:
        self._mock = mock

    def getQs(self: Qs) -> Dict[str, str]:
        return dict(
            map(
                lambda x: x.split("="),
                self._mock.call_args.args[0][0].split("?")[1].split("&"),
            )
        )

    def getPath(self: Qs) -> str:
        return urlparse(self._mock.call_args.args[0][0]).path


def TrackRequests(func: Callable) -> Callable[[Any, Qs], None]:
    @patch.object(_Query._Query, "_exec")
    def wrapper(self: Any, mock: Mock) -> None:
        func(self, Qs(mock))

    return wrapper
