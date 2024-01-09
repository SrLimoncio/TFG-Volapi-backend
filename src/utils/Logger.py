import logging
import os
import traceback

files_logger = {"DEFAULT": "app.log", "REQUESTS": "api_requests.log"}
log_filename = files_logger["DEFAULT"]


class Logger():
    def __set_logger(self):
        log_directory = 'src/utils/log'

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger

    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)

            if (level == "critical"):
                logger.critical(message)
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                logger.error(message)
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)

    @classmethod
    def set_file_logger(cls, type):
        log_filename = files_logger[type]
