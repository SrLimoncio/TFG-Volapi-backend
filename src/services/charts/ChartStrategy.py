from abc import ABC, abstractmethod
from src.services.charts.ChartBuilder import (SunburstChartBuilder,
                                              TimelineChartBuilder)


class ChartStrategy(ABC):
    @abstractmethod
    def get_builder(self, chart_type):
        pass


class ChartFactory(ChartStrategy):
    def get_builder(self, chart_type):
        if chart_type == 1:  # SunburstChart
            return SunburstChartBuilder()

        elif chart_type == 2:  # TimelineChart
            return TimelineChartBuilder()

        else:
            raise ValueError("Error al determinar el constructor de graficos")