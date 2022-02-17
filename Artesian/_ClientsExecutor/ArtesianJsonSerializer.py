from collections import defaultdict
from datetime import datetime
from dateutil import parser
import jsons
from typing import Callable, Dict, Optional, get_args

def __artesianDatetimeSerializer(
    obj:datetime,
    **kwargs) -> str:
    
  if (obj.tzinfo is None):
    ret = obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return ret
  offset = obj.utcoffset()
  if (offset is not None and offset.total_seconds() == 0):
    ret = obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ret
  ret = obj.isoformat(timespec='seconds')
  return ret

def __artesianDatetimeDeserializer(
    obj:str,
    *args,
    **kwargs) -> datetime:
  return parser.isoparse(obj)

def __camelToPascal(k:str)->str:
  return k[0].upper() + k[1:]

def __pascalToCamel(k:str)->str:
  return k[0].lower() + k[1:]

def __is_valid_json_key(key: object) -> bool:
    return issubclass(type(key), (str, int, float, bool)) or key is None
  
def __artesianDictSerializer(
    obj: dict,
    *,
    key_transformer: Optional[Callable[[str], str]] = None,
    **kwargs) -> list:
  result = []
  for key in obj:
    obj_ = obj[key]
    key_ = key if __is_valid_json_key(key) else jsons.dump(key, 
      key_transformer=None, 
      **kwargs)
    elem = jsons.dump(
      obj_,
      key_transformer=key_transformer,
      **kwargs)
    result.append({'Key': key_, 'Value': elem})
  return result

def __artesianDictDeserializer(
    obj: list,
    cls: type,
    *args,
    **kwargs) -> object:
  key, value = get_args(cls)
  result:Dict[key,value] = {
    jsons.load(item['Key'], key, *args, **kwargs):jsons.load(item['Value'], value, *args, **kwargs)
    for item in obj
  }
  return result
  
__artesianJsonSerializer = jsons.JsonSerializable.fork()

jsons.set_serializer(__artesianDictSerializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer)
jsons.set_deserializer(__artesianDictDeserializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer)

jsons.set_serializer(__artesianDatetimeSerializer, datetime, high_prio=True, fork_inst=__artesianJsonSerializer)
jsons.set_deserializer(__artesianDatetimeDeserializer, datetime, high_prio=True, fork_inst=__artesianJsonSerializer)


__artesianJsonKwArgs = {
  'strip_privates': True,
  'strip_nulls': True,
  #'strict': True, disabled due to failure in untyped Dict (Tags)
  'use_enum_name': True,
  'fork_inst': __artesianJsonSerializer,
}

def artesianJsonSerialize(obj: object, cls: type = None, **kwargs) -> object:
  """ 
      Sets the Artesian Json Serializer.

      Args:
        obj: string for the object for the serialization
        cls: type for the serialization
        kwargs: override the dump
      
      Returns:
        JsonSerializer.
  """
  kwargs_ = {**__artesianJsonKwArgs, **kwargs}
  return jsons.dump(obj, cls, key_transformer=__camelToPascal, **kwargs_)

def artesianJsonDeserialize(obj: object, cls: type = None, **kwargs) -> object:
  """ 
      Sets the Artesian Json Deserializer.

      Args:
        obj: string for the object for the deserialization
        cls: type for the deserialization
        kwargs: override the load
      
      Returns:
        JsonDeserializer.
  """
  kwargs_ = {**__artesianJsonKwArgs, **kwargs, 'strict': False}
  return jsons.load(obj, cls, key_transformer=__pascalToCamel, **kwargs_)