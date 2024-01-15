from typing import Protocol


class Forecaster(Protocol):
    def fit(self, data: list[float]) -> None:
        ...

    def forecast(self, time_units: int) -> float:
        ... 


class HoltWinters:


    def fit(self, data: list[float]) -> None:
        ...
    
    def forecast(self, time_units: int) -> float:
        ...

