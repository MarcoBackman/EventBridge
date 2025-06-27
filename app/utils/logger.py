import logging
import colorlog

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
        handler = logging.StreamHandler()
        
        log_colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors=log_colors,
            reset=True, # Resets color after the message
            # secondary_log_colors={ # Optional: for parts of the message
            #     'message': {
            #         'ERROR': 'red',
            #         'CRITICAL': 'red'
            #     }
            # }
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)