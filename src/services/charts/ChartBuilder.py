from abc import ABC, abstractmethod
import traceback
import pandas as pd
from io import StringIO
import json

# Logger
from src.utils.Logger import Logger


class ChartBuilder(ABC):
    @abstractmethod
    def build_chart(self, data):
        pass


class SunburstChartBuilder(ChartBuilder):
    def build_child_node(self, data, parent_node):
        # Construir nodos hijos para un PID padre específico
        children_nodes = [proc for proc in data if proc[1] == parent_node]
        result = []
        for child in children_nodes:
            child_node = {
                'name': child[2],
                'pid': child[0],
                'createTime': child[8],
                'exiteTime': child[9],
                'threads': int(child[4]) if child[4].isdigit() else 0,
                'children': self.build_child_node(data, child[0]),
                'value': int(child[4]) if child[4].isdigit() else 1
            }
            result.append(child_node)
        return result

    def build_root_nodes(self, data):
        # Encontrar PIDs raíz
        all_pids = {proc[0] for proc in data}
        root_nodes = []
        for line in data:
            if line[1] == '0' or line[1] not in all_pids:
                root_node = {
                    'name': line[2],
                    'pid': line[0],
                    'createTime': line[8],
                    'exiteTime': line[9],
                    'threads': int(line[4]) if line[4].isdigit() else 0,
                    'children': self.build_child_node(data, line[0]),
                    'value': int(line[4]) if line[4].isdigit() else 1
                }
                root_nodes.append(root_node)
        return root_nodes

    def build_chart(self, data):
        try:
            if 'values' in data and isinstance(data['values'], list):
                root_nodes  = self.build_root_nodes(data['values'])
                return {'name': 'root', 'children': root_nodes}
            else:
                raise ValueError("Los datos de entrada no tienen el formato esperado")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


class TimelineChartBuilder(ChartBuilder):
    def build_chart(self, data):
        pass
