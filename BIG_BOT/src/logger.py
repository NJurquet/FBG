import logging
import os

# Create a logs directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_directory, exist_ok=True)

# To select the level of logging :
#       => Change the logging parameter to one of the following :
#           - logging.DEBUG
#           - logging.INFO
#           - logging.WARNING
#           - logging.ERROR
#           - logging.CRITICAL

# Format of the log message :
# 01 Jan 2021 12:00:00 - __main__ - INFO - This is an info message

# Format of the time "%d %b %Y %H:%M:%S" => example : 01 Jan 2021 12:00:00

# Destination File : debug.log in the logs directory (FBG/BIG_BOT/logs/debug.log)

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%d %b %Y %H:%M:%S",
                    handlers=[
                        logging.FileHandler(os.path.join(log_directory, 'debug.log'))
                    ])

# Use this logger across the project to log messages (with the same name as this module)

logger = logging.getLogger(__name__)