from datetime import date, datetime
from enum import Enum
from platform import system
from dateutil import parser
import jsons
from typing import Any, Callable, Dict, Optional, Type, TypeVar, get_args


TEnum = TypeVar("TEnum", bound=Enum)


__commonFmt = "%Y-%m-%dT%H:%M:%S.%f"
if system() == "Linux":
    __commonFmt = "%04Y-%m-%dT%H:%M:%S.%f"


def __artesianDatetimeSerializer(obj: datetime, **kwargs: Any) -> str:
    if obj.tzinfo is None:
        ret = obj.strftime(__commonFmt)
        return ret
    offset = obj.utcoffset()
    if offset is not None and offset.total_seconds() == 0:
        ret = obj.strftime(__commonFmt + "Z")
        return ret
    ret = obj.isoformat(timespec="seconds")
    return ret


def __artesianDatetimeDeserializer(obj: str, *args: Any, **kwargs: Any) -> datetime:
    return parser.isoparse(obj)


def __checkResultExtractSerializer(
    obj: Any, *args: Any, **kwargs: Any
) -> Dict[str, object]:
    result: Dict[str, object] = {
        "AID": obj.assignmentId,
        "MKID": obj.marketDataId,
        "RID": obj.ruleId,
        "T": __artesianDatetimeSerializer(obj.time),
        "D": obj.issueCount,
        "S": __artesianDatetimeSerializer(obj.competenceStart),
        "E": __artesianDatetimeSerializer(obj.competenceEnd),
    }
    if obj.providerName is not None:
        result["P"] = obj.providerName
    if obj.curveName is not None:
        result["C"] = obj.curveName
    if obj.ruleName is not None:
        result["R"] = obj.ruleName
    if type(obj).__name__ == "CheckResultExtractVts" and obj.version is not None:
        result["V"] = __artesianDatetimeSerializer(obj.version)
    return result


def __checkResultExtractDeserializer(
    obj: Dict[str, object], cls: type, *args: Any, **kwargs: Any
) -> object:
    values = {
        "providerName": obj.get("P"),
        "curveName": obj.get("C"),
        "ruleName": obj.get("R"),
        "assignmentId": obj.get("AID", 0),
        "marketDataId": obj.get("MKID", 0),
        "ruleId": obj.get("RID", 0),
        "time": __artesianDatetimeDeserializer(str(obj["T"])),
        "issueCount": obj["D"],
        "competenceStart": __artesianDatetimeDeserializer(str(obj["S"])),
        "competenceEnd": __artesianDatetimeDeserializer(str(obj["E"])),
    }
    if cls.__name__ == "CheckResultExtractVts":
        version = obj.get("V")
        values["version"] = (
            __artesianDatetimeDeserializer(str(version)) if version is not None else None
        )
    return cls(**values)


def __enumValue(enumType: Type[TEnum], value: object) -> TEnum:
    if isinstance(value, enumType):
        return value
    return enumType[str(value)]


def __scheduleDefinitionDeserializer(
    obj: Dict[str, Any], *args: Any, **kwargs: Any
) -> Any:
    from Artesian.MarketData._Dto.CronScheduleDefinitionDto import (
        CronScheduleDefinitionDto,
    )
    from Artesian.MarketData._Enum.ScheduleDefinitionType import (
        ScheduleDefinitionType,
    )

    scheduleType = __enumValue(ScheduleDefinitionType, obj["Type"])
    if scheduleType is ScheduleDefinitionType.Cron:
        return CronScheduleDefinitionDto(
            cronExpression=obj.get("CronExpression"),
            timeZone=obj.get("TimeZone"),
        )
    raise ValueError(f"Unsupported schedule definition type: {scheduleType}")


def __triggerConfigDeserializer(
    obj: Dict[str, Any], *args: Any, **kwargs: Any
) -> Any:
    from Artesian.MarketData._Dto.TriggerConfigDto import (
        OnEventTriggerConfigDto,
        ScheduleTriggerConfigDto,
    )
    from Artesian.MarketData._Enum.AlertType import AlertType

    alertType = __enumValue(AlertType, obj["Type"])
    if alertType is AlertType.OnEvent:
        return OnEventTriggerConfigDto()
    if alertType is AlertType.Scheduled:
        return ScheduleTriggerConfigDto(
            scheduleDefinition=__scheduleDefinitionDeserializer(
                obj["ScheduleDefinition"]
            )
        )
    raise ValueError(f"Unsupported alert type: {alertType}")


def __dataQualityRuleConfigDeserializer(
    obj: Dict[str, Any], *args: Any, **kwargs: Any
) -> Any:
    from Artesian.MarketData._Dto.ActualCompletenessAndFreshnessConfigDto import (
        ActualCompletenessAndFreshnessConfigDto,
    )
    from Artesian.MarketData._Dto.DataQualityRuleConfigDto import (
        DataQualityRuleConfigDto,
    )
    from Artesian.MarketData._Dto.OutlierAbsoluteBoundConfigDto import (
        OutlierAbsoluteBoundConfigDto,
    )
    from Artesian.MarketData._Dto.OutlierConfigDto import OutlierConfigDto
    from Artesian.MarketData._Dto.OutlierRefCurveConfigDto import (
        OutlierRefCurveConfigDto,
    )
    from Artesian.MarketData._Dto.RecordValidationConfigDto import (
        RecordValidationConfigDto,
    )
    from Artesian.MarketData._Dto.ScheduleConfigDto import ScheduleConfigDto
    from Artesian.MarketData._Dto.VersionedCompletenessAndFreshnessConfigDto import (
        VersionedCompletenessAndFreshnessConfigDto,
    )
    from Artesian.MarketData._Enum.MarketDataType import MarketDataType
    from Artesian.MarketData._Enum.OutlierModel import OutlierModel
    from Artesian.MarketData._Enum.PeriodPrecision import PeriodPrecision
    from Artesian.MarketData._Enum.RuleType import RuleType

    ruleType = __enumValue(RuleType, obj["Type"])
    if ruleType is RuleType.Outlier:
        if "Model" not in obj:
            return DataQualityRuleConfigDto(type=ruleType)
        modelObj = obj["Model"]
        modelType = __enumValue(OutlierModel, modelObj["Model"])
        if modelType is OutlierModel.AbsoluteBound:
            model = OutlierAbsoluteBoundConfigDto(
                upperBound=modelObj["UpperBound"], lowerBound=modelObj["LowerBound"]
            )
        elif modelType is OutlierModel.RefCurve:
            model = OutlierRefCurveConfigDto(
                referenceMarketDataId=modelObj["ReferenceMarketDataId"],
                tolerancePerc=modelObj["TolerancePerc"],
            )
        else:
            raise ValueError(f"Unsupported outlier model: {modelType}")
        return OutlierConfigDto(model=model)

    if "MarketDataType" not in obj:
        return DataQualityRuleConfigDto(type=ruleType)
    marketDataType = __enumValue(MarketDataType, obj["MarketDataType"])
    scheduleObj = obj["ScheduleConfig"]
    scheduleConfig = ScheduleConfigDto(
        scheduleDefinition=__scheduleDefinitionDeserializer(
            scheduleObj["ScheduleDefinition"]
        ),
        maxDelay=scheduleObj["MaxDelay"],
    )
    validationObj = obj["RecordValidationConfig"]
    precision = validationObj.get("Precision")
    recordValidationConfig = RecordValidationConfigDto(
        recordRangeFrom=validationObj["RecordRangeFrom"],
        recordRangeTo=validationObj["RecordRangeTo"],
        precision=(
            __enumValue(PeriodPrecision, precision) if precision is not None else None
        ),
    )
    commonValues = {
        "marketDataType": marketDataType,
        "scheduleConfig": scheduleConfig,
        "recordValidationConfig": recordValidationConfig,
    }
    if marketDataType is MarketDataType.ActualTimeSerie:
        return ActualCompletenessAndFreshnessConfigDto(**commonValues)
    if marketDataType is MarketDataType.VersionedTimeSerie:
        versionPrecision = obj.get("VersionPrecision")
        return VersionedCompletenessAndFreshnessConfigDto(
            **commonValues,
            versionToleranceFrom=obj["VersionToleranceFrom"],
            versionToleranceTo=obj["VersionToleranceTo"],
            versionPrecision=(
                __enumValue(PeriodPrecision, versionPrecision)
                if versionPrecision is not None
                else None
            ),
        )
    raise ValueError(f"Unsupported Market Data type: {marketDataType}")


def __dataQualityStatusSummarySerializer(
    obj: Any, *args: Any, **kwargs: Any
) -> Dict[str, object]:
    result: Dict[str, object] = {
        "ActiveRulesCount": obj.activeRulesCount,
        "FailedRulesCount": obj.failedRulesCount,
    }
    if obj.lastCheckTime is not None:
        result["LastCheckTime"] = __artesianDatetimeSerializer(obj.lastCheckTime)
    if obj.overallStatus is not None:
        result["OverallStatus"] = obj.overallStatus.name
    if obj.from_ is not None:
        result["From"] = obj.from_.isoformat()
    if obj.to is not None:
        result["To"] = obj.to.isoformat()
    return result


def __dataQualityStatusSummaryDeserializer(
    obj: Dict[str, Any], *args: Any, **kwargs: Any
) -> Any:
    from Artesian.MarketData._Dto.DataQualityStatusSummaryDto import (
        DataQualityStatusSummaryDto,
    )
    from Artesian.MarketData._Enum.CheckAggregatedStatus import (
        CheckAggregatedStatus,
    )

    lastCheckTime = obj.get("LastCheckTime")
    overallStatus = obj.get("OverallStatus")
    fromValue = obj.get("From")
    toValue = obj.get("To")
    return DataQualityStatusSummaryDto(
        lastCheckTime=(
            __artesianDatetimeDeserializer(str(lastCheckTime))
            if lastCheckTime is not None
            else None
        ),
        overallStatus=(
            __enumValue(CheckAggregatedStatus, overallStatus)
            if overallStatus is not None
            else None
        ),
        activeRulesCount=obj.get("ActiveRulesCount", 0),
        failedRulesCount=obj.get("FailedRulesCount", 0),
        from_=date.fromisoformat(str(fromValue)) if fromValue is not None else None,
        to=date.fromisoformat(str(toValue)) if toValue is not None else None,
    )


def __camelToPascal(k: str) -> str:
    return k[0].upper() + k[1:]


def __pascalToCamel(k: str) -> str:
    return k[0].lower() + k[1:]


def __is_valid_json_key(key: object) -> bool:
    return issubclass(type(key), (str, int, float, bool)) or key is None


def __artesianDictSerializer(
    obj: dict, *, key_transformer: Optional[Callable[[str], str]] = None, **kwargs: Any
) -> list:
    result = []
    for key in obj:
        obj_ = obj[key]
        key_ = (
            key
            if __is_valid_json_key(key)
            else jsons.dump(key, key_transformer=None, **kwargs)
        )
        elem = jsons.dump(obj_, key_transformer=key_transformer, **kwargs)
        result.append({"Key": key_, "Value": elem})
    return result


def __artesianDictDeserializer(
    obj: list, cls: type, *args: Any, **kwargs: Any
) -> object:
    key, value = get_args(cls)
    result: Dict[key, value] = {  # type: ignore
        jsons.load(item["Key"], key, *args, **kwargs): jsons.load(
            item["Value"], value, *args, **kwargs
        )
        for item in obj
    }

    return result


__artesianJsonSerializer = jsons.JsonSerializable.fork()

jsons.set_serializer(
    __artesianDictSerializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer
)
jsons.set_deserializer(
    __artesianDictDeserializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer
)

jsons.set_serializer(
    __artesianDatetimeSerializer,
    datetime,
    high_prio=True,
    fork_inst=__artesianJsonSerializer,
)
jsons.set_deserializer(
    __artesianDatetimeDeserializer,
    datetime,
    high_prio=True,
    fork_inst=__artesianJsonSerializer,
)
__dataQualitySerializersRegistered = False


def __registerDataQualitySerializers() -> None:
    global __dataQualitySerializersRegistered
    if __dataQualitySerializersRegistered:
        return

    from Artesian.MarketData._Dto.CheckResultExtract import (
        CheckResultExtractTs,
        CheckResultExtractVts,
    )
    from Artesian.MarketData._Dto.DataQualityRuleConfigDto import (
        DataQualityRuleConfigDto,
    )
    from Artesian.MarketData._Dto.DataQualityStatusSummaryDto import (
        DataQualityStatusSummaryDto,
    )
    from Artesian.MarketData._Dto.ScheduleDefinitionDto import ScheduleDefinitionDto
    from Artesian.MarketData._Dto.TriggerConfigDto import TriggerConfigDto

    for cls in (CheckResultExtractTs, CheckResultExtractVts):
        jsons.set_serializer(
            __checkResultExtractSerializer,
            cls,
            high_prio=True,
            fork_inst=__artesianJsonSerializer,
        )
        jsons.set_deserializer(
            __checkResultExtractDeserializer,
            cls,
            high_prio=True,
            fork_inst=__artesianJsonSerializer,
        )
    jsons.set_deserializer(
        __dataQualityRuleConfigDeserializer,
        DataQualityRuleConfigDto,
        high_prio=True,
        fork_inst=__artesianJsonSerializer,
    )
    jsons.set_deserializer(
        __scheduleDefinitionDeserializer,
        ScheduleDefinitionDto,
        high_prio=True,
        fork_inst=__artesianJsonSerializer,
    )
    jsons.set_deserializer(
        __triggerConfigDeserializer,
        TriggerConfigDto,
        high_prio=True,
        fork_inst=__artesianJsonSerializer,
    )
    jsons.set_serializer(
        __dataQualityStatusSummarySerializer,
        DataQualityStatusSummaryDto,
        high_prio=True,
        fork_inst=__artesianJsonSerializer,
    )
    jsons.set_deserializer(
        __dataQualityStatusSummaryDeserializer,
        DataQualityStatusSummaryDto,
        high_prio=True,
        fork_inst=__artesianJsonSerializer,
    )
    __dataQualitySerializersRegistered = True


__artesianJsonKwArgs = {
    "strip_privates": True,
    "strip_nulls": True,
    # 'strict': True, disabled due to failure in untyped Dict (Tags)
    "use_enum_name": True,
    "fork_inst": __artesianJsonSerializer,
}


def artesianJsonSerialize(
    obj: object, cls: Optional[type] = None, **kwargs: Any
) -> object:
    """
    Sets the Artesian Json Serializer.

    Args:
      obj: string for the object for the serialization
      cls: type for the serialization
      kwargs: override the dump

    Returns:
      JsonSerializer.
    """
    __registerDataQualitySerializers()
    kwargs_ = {**__artesianJsonKwArgs, **kwargs}
    return jsons.dump(obj, cls, key_transformer=__camelToPascal, **kwargs_)


def artesianJsonDeserialize(
    obj: object, cls: Optional[type] = None, **kwargs: Any
) -> object:
    """
    Sets the Artesian Json Deserializer.

    Args:
      obj: string for the object for the deserialization
      cls: type for the deserialization
      kwargs: override the load

    Returns:
      JsonDeserializer.
    """
    __registerDataQualitySerializers()
    kwargs_ = {**__artesianJsonKwArgs, **kwargs, "strict": False}
    return jsons.load(obj, cls, key_transformer=__pascalToCamel, **kwargs_)
