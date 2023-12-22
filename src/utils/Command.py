import traceback
import subprocess
import os

# Logger
from src.utils.Logger import Logger


class Command:
    volatility_route = r"C:\Users\jose_\Documents\GitHub\TFG-Volapi\VolatilityCode\volatility3\Vol.py"

    @classmethod
    def execute_command_windows(cls, memory_dump_path, command_name, command_parameters):
        try:
            command = f"python {cls.volatility_route} -f {memory_dump_path} windows.{command_name}"
            #command = f"volatility -f {memory_dump_path} windows.{command_name}"
            if command_parameters:
                command += f" {command_parameters}"

            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            return result

        except Exception as ex:
            Logger.add_to_log("error", str(ex))
            Logger.add_to_log("error", traceback.format_exc())
