import traceback
import yara

# Logger
from src.utils.Logger import Logger

from src.utils.exceptions.error_handlers.SecurityErrorHandler import SecurityErrorHandler


class YaraService:
    @classmethod
    @SecurityErrorHandler.security_error_handler
    def execute_yara_rule(cls):
        # Ruta al archivo de reglas YARA
        path_file_yara_rule = r"C:\Users\jose_\Documents\GitHub\TFG-Volapi\VolatilityCode\YaraRules\malware_index.yar"
        # Ruta al volcado de memoria
        memory_dump_path = r"C:\Users\jose_\Downloads\stuxnet.vmem\stuxnet.vmem"

        try:
            # Compilar las reglas de YARA
            rules = yara.compile(filepath=path_file_yara_rule)

            # Leer el volcado de memoria
            with open(memory_dump_path, 'rb') as f:
                memory_data = f.read()

            # Ejecutar las reglas de YARA sobre el volcado de memoria
            matches = rules.match(data=memory_data)

            if not matches:
                Logger.add_to_log("info", "No se encontraron coincidencias.")
                return "No se encontraron coincidencias."

            # Procesar y mostrar los resultados
            for match in matches:
                Logger.add_to_log("info", f"Regla: {match.rule}")
                Logger.add_to_log("info", f"Regla: {match}")
                for string in match.strings:
                    offset, identifier, value = string
                    Logger.add_to_log("info", f"  Encontrado: {identifier} en {hex(offset)}: {value}")
                    print(f"  Encontrado: {identifier} en {hex(offset)}: {value}")

            return matches

        except Exception as e:
            print(f"Error: {e}")
            return None
