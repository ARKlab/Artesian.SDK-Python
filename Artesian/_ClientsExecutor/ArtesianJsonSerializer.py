import jsons
from Artesian._Services.Dto import ArtesianTags
from typing import List
from typish import instance_of

def __artesianTagsSerializer(
        obj: ArtesianTags,
        **kwargs) -> list:
  return [{'Key': k, 'Value': v} for k,v in obj.items()]

def __artesianTagsDeserializer(
        obj: list,
        cls: type,
        **kwargs) -> ArtesianTags:
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

__artesianJsonSerializer = jsons.JsonSerializable.fork()
jsons.set_serializer(__artesianTagsSerializer, ArtesianTags, high_prio=True, fork_inst=__artesianJsonSerializer)
jsons.set_deserializer(__artesianTagsDeserializer, ArtesianTags, high_prio=True, fork_inst=__artesianJsonSerializer)


__artesianJsonKwArgs = {
  'strip_privates': True,
  'strict': True,
  'use_enum_name': True,
  'fork_inst': __artesianJsonSerializer,
}

def artesianJsonSerialize(obj: str, cls: type = None, **kwargs: list[str]):
  """ 
      Sets the Artesian Json Serializer.

      Args:
        obj: string for the object for the serialization
        cls: type for the serialization
        kwargs: list of strings for the serialization
      
      Returns:
        JsonSerializer.
  """
  kwargs_ = {**__artesianJsonKwArgs, **kwargs}
  return jsons.dump(obj, cls, key_transformer=jsons.KEY_TRANSFORMER_PASCALCASE, **kwargs_)

def artesianJsonDeserialize(obj: str, cls: type = None, **kwargs: list[str]):
  """ 
      Sets the Artesian Json Deserializer.

      Args:
        obj: string for the object for the deserialization
        cls: type for the deserialization
        kwargs: list of strings for the deserialization
      
      Returns:
        JsonDeserializer.
  """
  kwargs_ = {**__artesianJsonKwArgs, **kwargs, 'strict': False}
  return jsons.load(obj, cls, key_transformer=jsons.KEY_TRANSFORMER_CAMELCASE, **kwargs_)