import math
import copy
class DefaultPartitionStrategy:
    maxNumberOfIds = 15
    
    def PartitionActual(self, actualQueryParameters):
        res = []
        for param in actualQueryParameters:
            if(param.ids is None):
                res.append(param)
                continue
            leng = len(param.ids)
            batches = [param.ids[i:i + DefaultPartitionStrategy.maxNumberOfIds] for i in range(0, leng, DefaultPartitionStrategy.maxNumberOfIds)]
            for batch in batches:
                cpParam = copy.deepcopy(param)
                cpParam.ids = batch
                res.append(cpParam)
        return res    
    def Partitionversioned(self, versionedQueryParameters):
        res = []
        for param in versionedQueryParameters:
            if(param.ids is None):
                res.append(param)
                continue
            leng = len(param.ids)
            batches = [param.ids[i:i + DefaultPartitionStrategy.maxNumberOfIds] for i in range(0, leng, DefaultPartitionStrategy.maxNumberOfIds)]
            for batch in batches:
                cpParam = copy.deepcopy(param)
                cpParam.ids = batch
                res.append(cpParam)
        return res
    def PartitionMas(self, masQueryParameters):
        res = []
        for param in masQueryParameters:
            if(param.ids is None):
                res.append(param)
                continue
            leng = len(param.ids)
            batches = [param.ids[i:i + DefaultPartitionStrategy.maxNumberOfIds] for i in range(0, leng, DefaultPartitionStrategy.maxNumberOfIds)]
            for batch in batches:
                cpParam = copy.deepcopy(param)
                cpParam.ids = batch
                res.append(cpParam)
        return res 


