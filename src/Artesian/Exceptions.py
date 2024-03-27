from __future__ import annotations
from typing import Optional


class ArtesianSdkException(Exception):
    """
    Base class for all `Artesian` errors.
    """

    def __init__(self: ArtesianSdkException, message: str) -> None:
        """
        Inits the Artesian Sdk Exception.

        Args:
            message: the message describing the problem.
        """
        Exception.__init__(self, message)
        self._message = message

    @property
    def message(self: ArtesianSdkException) -> str:
        return self._message


class ArtesianSdkRemoteException(ArtesianSdkException):
    """
    Artesian generic remote exception.
    """

    def __init__(
        self: ArtesianSdkRemoteException,
        method: str,
        url: str,
        statusCode: int,
        problemDetails: Optional[dict] = None,
        errorText: Optional[str] = None,
    ) -> None:
        """
        Inits the Artesian Sdk Remote Exception.

        Args:
            method: the HTTP method used
            url: the url of the request
            statusCode: the response status code
            problemDetails: the returned problemDetails object (if any)
            errorText: the response as text if problem details are not provided
        """
        self._method = method
        self._url = url
        self._statusCode = statusCode
        self._problemDetails = problemDetails
        self._errorText = errorText

        if problemDetails is not None:
            detail = (
                problemDetails.get("detail", None)
                or problemDetails.get("title", None)
                or problemDetails.get("type", None)
            )
        else:
            detail = errorText

        params = {"method": method, "url": url, "statusCode": statusCode}
        message = (
            "Failed REST call to Artesian. "
            + "{method} {url} returned {statusCode}.".format(**params)
        )
        if detail is not None:
            message = message + " " + detail

        ArtesianSdkException.__init__(self, message)

    @property
    def method(self: ArtesianSdkRemoteException) -> str:
        return self._method

    @property
    def url(self: ArtesianSdkRemoteException) -> str:
        return self._url

    @property
    def statusCode(self: ArtesianSdkRemoteException) -> int:
        return self._statusCode

    @property
    def problemDetails(self: ArtesianSdkRemoteException) -> Optional[dict]:
        return self._problemDetails

    @property
    def errorText(self: ArtesianSdkRemoteException) -> Optional[str]:
        return self._errorText


class ArtesianSdkValidationException(ArtesianSdkRemoteException):
    """
    Artesian validation exception. Raised when the Artesian Service object fails.
    """

    def __init__(
        self: ArtesianSdkValidationException,
        method: str,
        url: str,
        statusCode: int,
        problemDetails: Optional[dict] = None,
        errorText: Optional[str] = None,
    ) -> None:
        """
        Inits the Artesian Sdk Validation Exception.

        Args:
            method: the HTTP method used
            url: the url of the request
            statusCode: the response status code
            problemDetails: the returned problemDetails object (if any)
            errorText: the response as text if problem details are not provided
        """
        ArtesianSdkRemoteException.__init__(
            self, method, url, statusCode, problemDetails, errorText
        )


class ArtesianSdkOptimisticConcurrencyException(ArtesianSdkRemoteException):
    """
    Artesian optimistic concurrency exception.
    """

    def __init__(
        self: ArtesianSdkOptimisticConcurrencyException,
        method: str,
        url: str,
        statusCode: int,
        problemDetails: Optional[dict] = None,
        errorText: Optional[str] = None,
    ) -> None:
        """
        Inits the Artesian Sdk Optimistic Concurrency Exception.

        Args:
            method: the HTTP method used
            url: the url of the request
            statusCode: the response status code
            problemDetails: the returned problemDetails object (if any)
            errorText: the response as text if problem details are not provided
        """
        ArtesianSdkRemoteException.__init__(
            self, method, url, statusCode, problemDetails, errorText
        )


class ArtesianSdkForbiddenException(ArtesianSdkRemoteException):
    """
    Artesian forbidden exception.
    """

    def __init__(
        self: ArtesianSdkForbiddenException,
        method: str,
        url: str,
        statusCode: int,
        problemDetails: Optional[dict] = None,
        errorText: Optional[str] = None,
    ) -> None:
        """
        Inits the Artesian Sdk Forbidden Exception.

        Args:
            method: the HTTP method used
            url: the url of the request
            statusCode: the response status code
            problemDetails: the returned problemDetails object (if any)
            errorText: the response as text if problem details are not provided
        """
        ArtesianSdkRemoteException.__init__(
            self, method, url, statusCode, problemDetails, errorText
        )


class ArtesianSdkServerException(ArtesianSdkRemoteException):
    """
    Artesian Server exception (5xx).
    """

    def __init__(
        self: ArtesianSdkServerException,
        method: str,
        url: str,
        statusCode: int,
        problemDetails: Optional[dict] = None,
        errorText: Optional[str] = None,
    ) -> None:
        """
        Inits the Artesian Sdk Server Exception.

        Args:
            method: the HTTP method used
            url: the url of the request
            statusCode: the response status code
            problemDetails: the returned problemDetails object (if any)
            errorText: the response as text if problem details are not provided
        """
        ArtesianSdkRemoteException.__init__(
            self, method, url, statusCode, problemDetails, errorText
        )


class ArtesianSdkRequestException(ArtesianSdkException):
    pass
