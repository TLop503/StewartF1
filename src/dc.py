from dataclasses import dataclass

@dataclass
class Driver:
    name: str
    position: int
    laps: int
    points: int