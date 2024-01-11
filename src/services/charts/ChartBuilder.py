from abc import ABC, abstractmethod
import traceback
import pandas as pd
from io import StringIO
import json
from collections import Counter
import datetime

# Logger
from src.utils.Logger import Logger


class ChartBuilder(ABC):
    @abstractmethod
    def build_chart(self, command_id, data):
        pass


class SunburstChartBuilder(ChartBuilder):
    def build_chart(self, command_id, data):
        pass


class PidHierarchySunburstChartBuilder(SunburstChartBuilder):
    def build_child_node(self, command_id, data, parent_node):
        # Construir nodos hijos para un PID padre específico
        children_nodes = [proc for proc in data if proc[1] == parent_node]
        result = []
        for child in children_nodes:
            child_node = {
                'name': child[2],
                'pid': child[0].replace('*', '').replace(' ', ''),
                'createTime': child[8],
                'exiteTime': child[9],
                'threads': int(child[4]) if child[4].isdigit() else 0,
                'children': self.build_child_node(command_id, data, child[0].replace('*', '').replace(' ', '')),
                'value': int(child[4]) if child[4].isdigit() else 1
            }
            result.append(child_node)
        return result

    def build_root_nodes(self, command_id, data):
        # Encontrar PIDs raíz
        all_pids = {proc[0].replace('*', '').replace(' ', '') for proc in data}
        root_nodes = []
        for line in data:
            if line[1] == '0' or line[1] not in all_pids:
                root_node = {
                    'name': line[2],
                    'pid': line[0].replace('*', '').replace(' ', ''),
                    'createTime': line[8],
                    'exiteTime': line[9],
                    'threads': int(line[4]) if line[4].isdigit() else 0,
                    'children': self.build_child_node(command_id, data, line[0].replace('*', '').replace(' ', '')),
                    'value': int(line[4]) if line[4].isdigit() else 1
                }
                root_nodes.append(root_node)
        return root_nodes

    def build_chart(self, command_id, data):
        try:
            if 'values' in data and isinstance(data['values'], list):
                root_nodes  = self.build_root_nodes(command_id, data['values'])
                return {'name': 'root', 'children': root_nodes}
            else:
                raise ValueError("Los datos de entrada no tienen el formato esperado")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


class GroupPidsSunburstChartBuilder(SunburstChartBuilder):
    def build_child_node(self, command_id, data, parent_node):
        # Construir nodos hijos para un PID padre específico
        children_nodes = [proc for proc in data if proc[0] == parent_node]
        result = []
        for child in children_nodes:
            child_node = {}
            if command_id == "14":
                child_node = {
                    'name': child[4],
                    'base': child[2],
                    'size': child[3],
                    'value': 1
                }
            elif command_id == "2":
                child_node = {
                    'name': child[3],
                    'base': child[2],
                    'major': child[4],
                    'minor': child[5],
                    'product': child[6],
                    'build': child[7],
                    'value': 1
                }

            result.append(child_node)
        return result

    def build_root_nodes(self, command_id, data):
        all_pids = {proc[0] for proc in data}
        pids_seen = set()
        root_nodes = []
        for line in data:
            if line[0] not in pids_seen:
                root_node = {
                    'name': line[1],
                    'pid': line[0],
                    'children': self.build_child_node(command_id, data, line[0])
                }
                pids_seen.add(line[0])
                root_nodes.append(root_node)
        return root_nodes

    def build_chart(self, command_id, data):
        try:
            if 'values' in data and isinstance(data['values'], list):
                root_nodes = self.build_root_nodes(command_id, data['values'])
                return {'name': 'root', 'children': root_nodes}
            else:
                raise ValueError("Los datos de entrada no tienen el formato esperado")
        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


class TimelineChartBuilder(ChartBuilder):
    def build_chart(self, command_id, data):
        # Extraer fechas de los eventos
        dates = [item[2].strip() for item in data['values'] if item[2] != 'N/A']

        # Convertir fechas a objetos datetime (asumiendo el formato 'YYYY-MM-DD HH:MM:SS')
        formatted_dates = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') for date in dates]

        # Contar eventos por fecha
        date_counts = Counter(formatted_dates)

        # Preparar datos para el gráfico
        graph_data = [{'date': date, 'count': count} for date, count in date_counts.items()]

        return graph_data
