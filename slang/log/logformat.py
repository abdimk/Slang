import logging


class CustomLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def __INFO__(self, message:str,trace_back:bool=False)->None:
        logging.info(f" {message}",exc_info=trace_back)

    def __ERROR__(self, message:str,trace_back:bool=False)->None:
        logging.error(f" {message}",exc_info=trace_back)

    def __DEBUG__(self, message:str, trace_back:bool=False)->None:
        logging.info(f" {message}",exc_info=trace_back)

