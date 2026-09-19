from water_monitor.water_level import WaterLevel


class WaterMonitor:
    FREQ_LEVELS = {
        WaterLevel.UNKNOWN: (-1, -1),
        WaterLevel.WITHOUT_LIQUID: (0, 40),  # 20Hz
        WaterLevel.DP_1_WITH_LIQUID: (41, 80),  # 50Hz
        WaterLevel.DP_2_WITH_LIQUID: (81, 150),  # 100 Hz
        WaterLevel.DP_3_WITH_LIQUID: (151, 280),  # 200 Hz
        WaterLevel.DP_4_WITH_LIQUID: (281, 1000),  # 400Hz
    }

    def map_frequency_to_level(self, freq: float) -> WaterLevel:
        for level, (low, high) in self.FREQ_LEVELS.items():
            if low <= freq <= high:
                return level
        return WaterLevel.UNKNOWN
