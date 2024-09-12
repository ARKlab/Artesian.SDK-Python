from __future__ import annotations
from typing import Optional

from Artesian.Query.DerivedQuery import DerivedQuery
from Artesian._ClientsExecutor.RequestExecutor import _RequestExecutor
from Artesian._ClientsExecutor.Client import _Client
from .DefaultPartitionStrategy import DefaultPartitionStrategy

from ._QueryParameters.VersionSelectionType import VersionSelectionType


class VersionedQuery(DerivedQuery):

    def __init__(
        self: VersionedQuery,
        client: _Client,
        requestExecutor: _RequestExecutor,
        partitionStrategy: DefaultPartitionStrategy,
    ) -> None:
        """Inits _VersionedQuery"""
        super().__init__(client, requestExecutor, partitionStrategy)

    def forMUV(
        self: VersionedQuery, versionLimit: Optional[str] = None
    ) -> VersionedQuery:
        """Gets the timeseries of the most updated version of each timepoint of
           a versioned timeseries.

        Args:
            versionLimit: string specifying a datetime from which the most updated
                          version should be taken, i.e. MUV as of (versionLimit).
                          Ex.: versionLimit("2021-03-12T14:30:00")

        Returns:
            VersionedQuery.
        """
        self._queryParameters.versionLimit = versionLimit
        self._queryParameters.versionSelectionType = VersionSelectionType.MUV
        return self

    def forLastOfDays(
        self: VersionedQuery, start: str, end: Optional[str] = None
    ) -> VersionedQuery:
        """Gets the lastest version of a versioned timeseries of each day
           in a time window..

        Args:
            start: string for the start timeseries for last of days.
                   ex.: forLastOfDays("2021-03-12",...),forLastOfDays("P0Y0M-2D", ...)
            end: string for the end timeseries for last of days.
                 ex.: forLastOfDays("2021-03-12","2021-03-16")
                       forLastOfDays("P0Y0M-2D","P0Y0M2D")

        Returns:
            VersionedQuery.
        """

        self._queryParameters.versionSelectionType = VersionSelectionType.LastOfDays
        vr = self._queryParameters.versionSelectionConfig.versionsRange
        if start.startswith("P"):
            if end is None:
                vr.period = start
            else:
                vr.periodFrom = start
                vr.periodTo = end
        else:
            vr.dateStart = start
            vr.dateEnd = end
        return self

    def forLastOfMonths(
        self: VersionedQuery, start: str, end: Optional[str] = None
    ) -> VersionedQuery:
        """Gets the lastest version of a versioned timeseries of each month
           in a time window.

        Args:
            start: string for the start timeseries for last of month.
                   ex: forLastOfMonths("2021-03-12",...),forLastOfMonths("P0Y-1M0D",...)
            end: string for the end timeseries for last of month.
                 ex: forLastOfMonths("2021-03-12","2021-03-16"),
                     forLastOfMonths("P0Y-1M0D","P0Y1M0D")

        Returns:
            VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.LastOfMonths
        vr = self._queryParameters.versionSelectionConfig.versionsRange
        if start.startswith("P"):
            if end is None:
                vr.period = start
            else:
                vr.periodFrom = start
                vr.periodTo = end
        else:
            vr.dateStart = start
            vr.dateEnd = end
        return self

    def forLastNVersions(self: VersionedQuery, lastN: int) -> VersionedQuery:
        """Gets the lastest N timeseries versions that have at least a not-null value .

        Args:
            lastN: an int > 0. Ex.: forLastNVersions(2)

        Returns:
            VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.LastN
        self._queryParameters.versionSelectionConfig.lastN = lastN
        return self

    def forVersion(self: VersionedQuery, version: str) -> VersionedQuery:
        """Gets the specified version of a versioned timeseries.

        Args:
            version: string of a specific version. Ex.:forVersion("2021-03-12T14:30:00")

        Returns:
            VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.Version
        self._queryParameters.versionSelectionConfig.version = version
        return self

    def forMostRecent(
        self: VersionedQuery, start: str, end: Optional[str] = None
    ) -> VersionedQuery:
        """Gets the most recent version of a versioned timeseries in a time window.

        Args:
            start: string for the start of the most recent version.
                   Ex.: (forMostRecent("2021-03-12",...))

            end: string for the end of the most recent version.
                 Ex.: (forMostRecent("2021-03-12","2021-03-16"))

        Returns:
            VersionedQuery.
        """
        self._queryParameters.versionSelectionType = VersionSelectionType.MostRecent
        vr = self._queryParameters.versionSelectionConfig.versionsRange
        if start.startswith("P"):
            if end is None:
                vr.period = start
            else:
                vr.periodFrom = start
                vr.periodTo = end
        else:
            vr.dateStart = start
            vr.dateEnd = end
        return self
