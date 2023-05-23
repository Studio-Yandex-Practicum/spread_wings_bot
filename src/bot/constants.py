from pathlib import Path

START_MESSAGE = 'Здесь выводится приветственное или информационное сообщение'
HELP_MESSAGE = 'Здесь выводится краткое описание возможностей бота'

BASE_DIR = Path(__name__).parent
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'