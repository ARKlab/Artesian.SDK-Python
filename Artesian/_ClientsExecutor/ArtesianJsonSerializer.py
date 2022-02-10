from datetime import datetime
from dateutil import parser
import jsons
from Artesian._Services.Dto import ArtesianTags
from typing import Callable, Dict, List, Optional
from typish import instance_of

def __artesianTagsSerializer(
        obj: ArtesianTags,
        **kwargs) -> list:
  if obj is None:
    return None
  return [{'Key': k, 'Value': v} for k,v in obj.items()]

def __artesianTagsDeserializer(
        obj: list,
        cls: type,
        **kwargs) -> ArtesianTags:
  if obj is None:
    return None
  result = ArtesianTags({})
  for item in obj:
    if (not instance_of(item['Key'], str)):
      raise ValueError("Key must be a 'str'. For example: 'commodity'") 
    if (not instance_of(item['Value'], List[str])):
      raise ValueError("Value must be a 'list[str]'. For example: ['gas','power']")

    k = jsons.load(item['Key'], str, **{**kwargs, 'strict':True})
    v = jsons.load(item['Value'], List[str], **{**kwargs, 'strict':True})
    result[k]=v
  
  return result

def __artesianDatetimeSerializer(
    obj:datetime,
    **kwargs) -> str:
    
  if (obj.tzinfo is None):
    ret = obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return ret
  if (obj.utcoffset().total_seconds() == 0):
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
    return any(issubclass(type(key), json_key) for json_key in (str, int, float, bool, type(None)))
  
def __artesianDictSerializer(
    obj: dict,
    *,
    key_transformer: Optional[Callable[[str], str]] = None,
    **kwargs) -> dict:
  result = dict()
  for key in obj:
    obj_ = obj[key]
    key_ = key if __is_valid_json_key(key) else jsons.dump(key, 
      key_transformer=None, 
      **kwargs)
    elem = jsons.dump(
      obj_,
      key_transformer=key_transformer,
      **kwargs)
    result[key_] = elem
  return result

__artesianJsonSerializer = jsons.JsonSerializable.fork()

jsons.set_serializer(__artesianDictSerializer, Dict, high_prio=True, fork_inst=__artesianJsonSerializer)

jsons.set_serializer(__artesianTagsSerializer, ArtesianTags, high_prio=True, fork_inst=__artesianJsonSerializer)
jsons.set_deserializer(__artesianTagsDeserializer, ArtesianTags, high_prio=True, fork_inst=__artesianJsonSerializer)

jsons.set_serializer(__artesianDatetimeSerializer, datetime, high_prio=True, fork_inst=__artesianJsonSerializer)
jsons.set_deserializer(__artesianDatetimeDeserializer, datetime, high_prio=True, fork_inst=__artesianJsonSerializer)


__artesianJsonKwArgs = {
  'strip_privates': True,
  'strip_nulls': True,
  'strict': True,
  'use_enum_name': True,
  'fork_inst': __artesianJsonSerializer,
}

def artesianJsonSerialize(obj: str, cls: type = None, **kwargs) -> dict:
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

def artesianJsonDeserialize(obj: str, cls: type = None, **kwargs) -> object:
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