from enum import Enum


class AggregationRule(Enum):
    Undefined = 0
    SumAndDivide = 1
    AverageAndReplicate = 2
