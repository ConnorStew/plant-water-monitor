from enum import Enum

# Frequency thresholds for each level

class WaterLevel(Enum):
    UNKNOWN = 0
    WITHOUT_LIQUID = 1
    DP_1_WITH_LIQUID = 2
    DP_2_WITH_LIQUID = 3
    DP_3_WITH_LIQUID = 4
    DP_4_WITH_LIQUID = 5