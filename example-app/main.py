import logging
import structlog
import sys
# from logging.handlers import TimedRotatingFileHandler
from logging.handlers import SocketHandler
import time

# def elastic_format(logger: logging.Logger, method_name: str, event_dict: dict):
#     # Elastic requires the message to be under 'message' and not under 'event'
#     if isinstance(event_dict, dict) and event_dict.get('event') and not event_dict.get('message'):
#         event_dict['message'] = event_dict.pop('event')
#     return event_dict

# Configure structlog
structlog.configure_once(
    processors=[
        structlog.stdlib.add_log_level,
        #structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.processors.StackInfoRenderer(),
        #structlog.processors.format_exc_info,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=False
)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(structlog.stdlib.ProcessorFormatter(processor=structlog.processors.JSONRenderer()))

# file_handler = TimedRotatingFileHandler(filename='./my_logs.log', interval=1, backupCount=48, encoding='utf-8')
# file_handler.setFormatter(structlog.stdlib.ProcessorFormatter(processor=structlog.processors.JSONRenderer()))

class FluentBitHandler(SocketHandler):
    def emit(self, record):
        try:
            self.send((self.format(record)).encode())
        except Exception:
            self.handleError(record)

socket_handler = FluentBitHandler("fluent-bit", 24224)
socket_handler.setFormatter(structlog.stdlib.ProcessorFormatter(processor=structlog.processors.JSONRenderer()))
# Set up root logger
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)
# root_logger.addHandler(file_handler)
root_logger.addHandler(socket_handler)
root_logger.setLevel('INFO')

# # Get a logger
# logger = structlog.getLogger('my_logger')
# logger.info('My log message.')

if __name__ == "__main__":
    IS_LOG_SIMULATOR_ACTIVE = True
    # Get a logger
    logger = structlog.getLogger('my_logger')
    while IS_LOG_SIMULATOR_ACTIVE:
        logger.info('Bye')
        time.sleep(10)
