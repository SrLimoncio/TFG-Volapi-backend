from abc import ABC, abstractmethod

from src.services.charts.ChartBuilder import (PidHierarchySunburstChartBuilder,
                                              GroupPidsSunburstChartBuilder,
                                              TimelineChartBuilder)


class ChartStrategy(ABC):
    @abstractmethod
    def get_builder(self, chart_type, command_id):
        """
        Método abstracto para obtener el constructor de gráficos.
        Debe ser implementado por subclases específicas.
        """
        pass


class ChartFactory(ChartStrategy):
    def get_builder(self, chart_type, command_id):
        """
        Obtiene el constructor de gráficos adecuado en función del tipo de gráfico y el ID del comando.

        Args:
            chart_type (int): Tipo de gráfico que se desea construir.
            command_id (str): ID del comando relacionado con el gráfico.

        Returns:
            ChartBuilder: Una instancia de un constructor de gráficos específico.

        Raises:
            ValueError: Si no se puede determinar el constructor de gráficos.
        """
        if chart_type == 1:  # SunburstChart
            if (command_id == "11"  # PSList
                    or command_id == "12"  # PSScan
                    or command_id == "13"):  # PSTree
                return PidHierarchySunburstChartBuilder()
            elif (command_id == "2"  # VerIndo
                  or command_id == "14"):  # DllList
                print(1)
                return GroupPidsSunburstChartBuilder()
            else:
                raise ValueError("Error al determinar el constructor de graficos")

        elif chart_type == 2:  # TimelineChart
            return TimelineChartBuilder()

        else:
            raise ValueError("Error al determinar el constructor de graficos")
