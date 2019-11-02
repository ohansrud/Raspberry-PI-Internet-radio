from pprint import pprint
import traceback
import logging
import os
from datetime import datetime
# using get will return `None` if a key is not present rather than raise a `KeyError`
PRINT_ENABLED = True
log_level = os.environ.get('LOG_LEVEL')

if(log_level == None):
    log_level = logging.ERROR

print(log_level)

logging.basicConfig(
    filename='/var/log/radio.log', 
    filemode='w', 
    level=log_level,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

def error_handler(error):
    if(PRINT_ENABLED):
        pprint(error)
        traceback.print_exc
        traceback.print_stack

    stack = traceback.format_stack()
    current_time = str(datetime.now())
    logging.error(current_time + ": " + str(error))
    logging.error(stack)


def console_logger(message):
    if(PRINT_ENABLED):
        pprint(message)
    logging.debug(message)
