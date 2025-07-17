from dataclasses import dataclass, fields


@dataclass(frozen=True)
class Pins:
    GREEN_LED: int = 17
    RED_LED: int = 23
    BLUE_LED: int = 22
    SENSOR: int = 18

    @classmethod
    def values(cls) -> list[int]:
        return [getattr(cls, f.name) for f in fields(cls)]