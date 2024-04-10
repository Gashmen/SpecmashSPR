import logging
import tempfile

class LoggerSapr:

    def __init__(self):
        self.logger_file_obj = tempfile.NamedTemporaryFile(delete=False)  # Создание временного файла
        self.logger_path = self.logger_file_obj.name  # Получение пути данного временного файла
        # Настройка логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger_file = logging.FileHandler(filename=self.logger_path)
        self.logger_file.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(name)s %(message)s'))
        self.logger.addHandler(self.logger_file)
        self.logger_file_obj.close()
        self.logger.info('Логгер установлен')

