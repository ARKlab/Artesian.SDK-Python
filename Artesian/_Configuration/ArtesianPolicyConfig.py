class ArtesianPolicyConfig:
    def __init__(self, maxRetry, retryWaitTime,  maxParallelism):
        if maxRetry is None:
            self.maxRetry = 5
        else:
            self.maxRetry = maxRetry
        if maxRetry is None:
            self.retryWaitTime = 200
        else:
            self.retryWaitTime = retryWaitTime
        if maxParallelism is None:
            self.maxParallelism = 3
        else:
            self.maxParallelism = maxParallelism
             