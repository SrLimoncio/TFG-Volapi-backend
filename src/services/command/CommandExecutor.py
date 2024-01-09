from abc import ABC, abstractmethod
import traceback
import subprocess
import os
from pathlib import Path

# Logger
from src.utils.Logger import Logger


class CommandExecutor(ABC):
    SHARED_ID_COMMANDS = ['timeliner.Timeliner',
                          'yarascan.YaraScan',
                          'banners.Banners',
                          'configwriter.ConfigWriter',
                          'frameworkinfo.FrameworkInfo',
                          'isfinfo.IsfInfo',
                          'layerwriter.LayerWriter']

    @abstractmethod
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class WindowsVol2Executor(CommandExecutor):
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class WindowsVol3Executor(CommandExecutor):
    def __init__(self):
        vol3_path = os.getenv("VOL3_PATH", r"VolatilityCode\volatility3\Vol.py")
        self.vol3_route = Path(vol3_path).resolve()

    def execute_command(self, memory_file_path, command_plugin_name, command_plugin_options):
        try:
            command = ["python", str(self.vol3_route), "-f", memory_file_path]
            memory_file_name = memory_file_path.split('\\')[-1]
            visible_command = f"python path\\volatility3\\Vol.py -f memory_dump_path\\{memory_file_name}"

            if command_plugin_name not in self.SHARED_ID_COMMANDS:
                line = f"windows.{command_plugin_name}"
                command.append(line)
                visible_command += (" " + line)
            else:
                command.append(command_plugin_name)
                visible_command += (" " + command_plugin_name)

            if command_plugin_options:
                for option in command_plugin_options:
                    command.append(option['code'])
                    visible_command += (' ' + option['code'])
                    if option['type'] == "with_arguments":
                        command.append(option['value'])
                        visible_command += (' ' + option['value'])

            Logger.add_to_log("info", str(command))

            result = subprocess.run(command, capture_output=True, text=True)
            # result = subprocess.run(command, shell=True, capture_output=True, text=True)

            return result, visible_command

        except Exception as ex:
            Logger.add_to_log("error", f"Error ejecutando {command_plugin_name}: {ex}")
            Logger.add_to_log("error", traceback.format_exc())
            return None, None


class LinuxVol2Executor(CommandExecutor):
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class LinuxVol3Executor(CommandExecutor):
    vol3_route = r"C:\Users\jose_\Documents\GitHub\TFG-Volapi\VolatilityCode\volatility3\Vol.py"

    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass
