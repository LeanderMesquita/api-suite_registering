from loguru import logger
import os

# Configurar o arquivo de log
log_file = os.path.join('logs', 'automation.log')
logger.add(log_file, rotation="1 MB", retention="10 days", level="INFO", format="{time} - {level} - {message}")

log = logger