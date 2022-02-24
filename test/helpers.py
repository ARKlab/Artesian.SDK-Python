
from unittest.mock import patch
import Artesian.Query._Query as _Query

def TrackRequests(func):
    @patch.object(_Query._Query, '_exec')
    def wrapper(self, mock):
        class Qs:
            def getQs(_self):
                return dict(map(lambda x:x.split('='), mock.call_args.args[0][0].split('?')[1].split('&')))

        func(self, Qs())
    return wrapper