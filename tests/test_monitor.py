import pytest

from water_monitor.monitor import WaterMonitor
from water_monitor.water_level import WaterLevel


@pytest.mark.parametrize(
    ("freq", "expected"),
    [
        (20, WaterLevel.WITHOUT_LIQUID),
        (50, WaterLevel.DP_1_WITH_LIQUID),
        (100, WaterLevel.DP_2_WITH_LIQUID),
        (200, WaterLevel.DP_3_WITH_LIQUID),
        (400, WaterLevel.DP_4_WITH_LIQUID),
        (5000, WaterLevel.UNKNOWN),
    ],
)
def test_map_frequency_to_level(freq, expected):
    assert WaterMonitor().map_frequency_to_level(freq) == expected
