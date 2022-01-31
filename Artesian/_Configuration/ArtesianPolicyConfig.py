class ArtesianPolicyConfig:
    """ 
         Artesian Policy Configuration

         The class for the configuration to the connection with Artesian where are specified the retry, the waiting time and the parallelism as parameters.

         Attributes:
             maxRetry: An int indicating the number of retries.
             retryWaitTime: An int indicating the time in milliseconds to wait fot the backoff.
             maxParallelism: An int indicating the maximum of executions through the bulkhead.
     """


    def __init__(self, maxRetry: int, retryWaitTime: int,  maxParallelism: int) -> None:
        """
             Inits Artesian Policy Config with optional overrides.
             
             Args:
                 maxRetry: the maximum numbers of retries. "(default:5)."

                 retryWaitTime: the wait time for exponential backoff in milliseconds. "(default:200)."
                 
                 maxParallelism: the maximum parallelization of executions through the bulkhead. "(default:3)." 
        """
        if maxRetry is None:
            self.maxRetry = 5
            
        else:
            self.maxRetry = maxRetry
        if retryWaitTime is None:
            self.retryWaitTime = 200
        else:
            self.retryWaitTime = retryWaitTime
        if maxParallelism is None:
            self.maxParallelism = 3
        else:
            self.maxParallelism = maxParallelism
             