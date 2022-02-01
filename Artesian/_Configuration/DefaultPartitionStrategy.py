import copy
class DefaultPartitionStrategy:
    maxNumberOfIds = 15
    
    def PartitionActual(self, actualQueryParameters):
        return self._tsPartitionStrategy(actualQueryParameters)
    def PartitionAuction(self, auctionQueryParameters):
        return self._tsPartitionStrategy(auctionQueryParameters)
    def Partitionversioned(self, versionedQueryParameters):
       return self._tsPartitionStrategy(versionedQueryParameters)
    def PartitionMas(self, masQueryParameters):
        return self._tsPartitionStrategy(masQueryParameters)
    def PartitionGMEPOffer(self, gmePOfferQueryParameters):
        return gmePOfferQueryParameters

    def _tsPartitionStrategy(self, Parameters):
        res = []
        for param in Parameters:
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

