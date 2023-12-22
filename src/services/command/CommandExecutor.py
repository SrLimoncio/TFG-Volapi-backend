from abc import ABC, abstractmethod
import traceback
import subprocess
import os

# Logger
from src.utils.Logger import Logger


class CommandExecutor(ABC):
    @abstractmethod
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class WindowsVol2Executor(CommandExecutor):
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class WindowsVol3Executor(CommandExecutor):
    vol3_route = r"C:\Users\jose_\Documents\GitHub\TFG-Volapi\VolatilityCode\volatility3\Vol.py"

    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        try:
            command = f"python {self.vol3_route} -f {memory_dump_path} windows.{command_plugin_name}"
            # command = f"volatility -f {memory_dump_path} windows.{command_name}"
            if command_plugin_options:
                command += f" {command_plugin_options}"

            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            name_memory_dump = memory_dump_path.split('\\')[-1]
            visible_command = (f"python path\\volatility3\\Vol.py "
                               f"-f memory_dump_path\\{name_memory_dump} "
                               f"windows.{command_plugin_name}")

            return result, visible_command

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())


class LinuxVol2Executor(CommandExecutor):
    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass


class LinuxVol3Executor(CommandExecutor):
    vol3_route = r"C:\Users\jose_\Documents\GitHub\TFG-Volapi\VolatilityCode\volatility3\Vol.py"

    def execute_command(self, memory_dump_path, command_plugin_name, command_plugin_options):
        pass
