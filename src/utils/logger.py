import sys
import os
import logging, coloredlogs
from datetime import datetime
from exceptions import (
    ClassNameNotFound,
    InvalidHandlerConfig,
    InvalidLogLevel
    )



file_logger = logging.getLogger(__file__)
file_handler = logging.FileHandler(f"logger-{datetime.now()}.log", mode="a")
file_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
file_logger.addHandler(file_handler)

console_logger = logging.getLogger(__file__)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
console_logger.addHandler(console_handler)


class Logger:
    """
    # Logger Class
    The Logger class is designed to provide an easy-to-use logging utility for your Python application. It supports various logging methods and allows you to customize the log level, log type (file or stream), and the log file name.

    ## Constructor
        - name (str): Name of the logger
        - handler_type (str): The type of handler for the     logger. Supported types are "file" and "stream".
        - log_level (int) : The number for log level for the logger. Supported levels are 0 to 4.
        - **kwargs: Additional keyword arguments for the logger.
    
    ## Methods:
    `set_func_name(self, func_name)`
        - func_name (str): The name of the function from which the log is being called.

        Sets the function name for the logger, which will be prepended to the log message, to make the logs more readable and easy to deduce the messages generated.

        Expects the class name to be set or else it will raise an Exception.

    `set_class_name(self, class_name)`
        - class_name (str): The name of the class from which the log is being called.

        Sets the class name for the logger , which will be prepended to the log message, to make the logs more readable and easy to deduce where the messages are generating from.

        Expects func_name to be set as well to log the name of the function being called.

        Set the class_name then set the func_name for proper use.

    `log(self, level, message)`
        - level (int): Level of the log. 
        - message (str):  Message to display in the log.
        
        **Log levels**
        + 0 = DEBUG
        + 1 = INFO
        + 2 = WARNING
        + 3 = ERROR
        + 4  = CRITICAL

        Logs the message at the specified log level. The available log levels are:

    ## Usage:
        ```python
        console_logger = Logger(__file__, "stream", "debug")
        file_logger = Logger(__file__, handler_type="file",
                     log_level="debug", filename="filename.log")
        ```
    """
    def __init__(
            self, name: str,
            handler_type: str, log_level: int, **kwargs):
        self.name = name
        self.supported_handler_type = ["file", "stream", "http", "https"]

        if handler_type not in self.supported_handler_type:
            return Exception(f"{handler_type} is not supported. {self.supported_handler_type} are the supported handler types.")
        
        self.handler_type = handler_type
        self.accepted_levels = ['debug', 'info', 'warning', 'error', 'critical']
        self.set_level_map = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'critical': logging.CRITICAL,
            'error': logging.ERROR
        }
        self.log_level = self.set_level_map[self.accepted_levels[log_level]]
        self.kwargs = kwargs
        self.logger = logging.getLogger(self.name)

        # class and function name for better logging
        self.__class_name = None
        self.__func_name = None

        # log configuration
        self.logger.setLevel(self.log_level)
        coloredlogs.install(fmt="%(levelname)s %(asctime)s %(message)s", level=self.log_level)
        console_logger.info("Initialized Logger class.")
        file_logger.debug(f"Initialized {self.name} Logger class and class name is set to {self.__class_name}; LogLevel: {self.log_level}")

    def add_handler(self) -> None:
        log_directory = "logs"
        if self.handler_type == "file":
            if "filename" in self.kwargs.keys():
                filename = os.path.abspath(log_directory+self.kwargs['filename'])
                file_handler = logging.FileHandler(filename, mode="a")
                self.logger.addHandler(file_handler)
                
            else:
                console_logger.error("`filename` argument missing for filetype handler.")
                file_logger.error("`filename` argument missing for filetype handler.")
                raise InvalidHandlerConfig("Please pass filename argument for filetype handler")

        if self.handler_type == "stream":
            stream_handler = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(stream_handler)
            console_logger.info("Added StreamHandler")
            file_logger.info("Added StreamHandler")
        
        if self.handler_type == "http" or self.handler_type == "https":
            print("Currently this handler type is not supported but will be in future.")
            print("Defaulting to stream handler.")
            stream_handler = logging.StreamHandler()
            self.logger.addHandler(stream_handler)
            print("Added StreamHandler")
    
    def set_class_name(self, class_name):
        self.__class_name = class_name
        # print(f"Logger set to {class_name}")
    
    def get_class_name(self):
        return self.__class_name
    
    def set_func_name(self, func_name):
        """
        Sets the function name.
        Expects that the class name has already been set otherwise raises an Exception.
        :param func_name: Name of the function
        """
        if self.__class_name:
            self.__func_name = func_name
            # print(f"Logger set to {func_name}")
        else:
            raise ClassNameNotFound('Class name has not been set yet. Set class name with set_class_name method.')
    
    def get_func_name(self):
        """
        Returns the set function name
        """
        return self.__func_name

    def remove_func_name(self):
        self.__func_name = None

    def log(self, level:int=0, message:str=""):
        """
        Logs the given message at the specified level. If no level is provided it defaults to 0 which is DEBUG.
        Arguments:
        level: int  -- The severity level of the log. Possible values are 0|1|2|3|4  (DEBUG|INFO|WARNING|ERROR|CRITICAL)
        message: str --  The actual log message that needs to be logged.
        """
        match level:
            case 0:
                if self.__class_name and self.__func_name:
                    self.logger.debug(f"{self.__class_name}.{self.__func_name}: {message}")
                    self.remove_func_name()
                elif self.__class_name is None:
                    self.logger.debug(message)
                    self.remove_func_name()
                else:
                    self.logger.warning("Function name has not been set for the logger.")
                    self.remove_func_name()
                
            
            case 1:
                if self.__class_name and self.__func_name:
                    self.logger.info(f"{self.__class_name}.{self.__func_name}: {message}")
                    self.remove_func_name()
                elif self.__class_name:
                    self.logger.info(f"{self.__class_name}.NA: {message}")
                    self.remove_func_name()
                else:
                    self.logger.info(message)
                    self.logger.warning("Function name has not been set for the logger.")
                    self.remove_func_name()
            
            case 2:
                if self.__class_name and self.__func_name:
                    self.logger.warning(f"{self.__class_name}.{self.__func_name}: {message}")
                    self.remove_func_name()
                elif self.__class_name:
                    self.logger.warning(f"{self.__class_name}.NA: {message}")
                    self.remove_func_name()
                else:
                    self.logger.warning(message)
                    self.logger.warning("Function name has not been set for the logger.")
                    self.remove_func_name()
            
            case 3:
                if self.__class_name and self.__func_name:
                    self.logger.error(f"{self.__class_name}.{self.__func_name}: {message}")
                    self.remove_func_name()
                elif self.__class_name:
                    self.logger.error(f"{self.__class_name}.NA: {message}")
                    self.remove_func_name()
                else:
                    self.logger.error(message)
                    self.logger.warning("Function name has not been set for the logger.")
                    self.remove_func_name()
            
            case 4:
                if self.__class_name and self.__func_name:
                    self.logger.critical(f"{self.__class_name}.{self.__func_name}: {message}")
                    self.remove_func_name()
                elif self.__class_name:
                    self.logger.critical(f"{self.__class_name}.NA: {message}")
                else:
                    self.logger.critical(message)
                    self.logger.warning("Function name has not been set for the logger.")
            
            case _:
                raise InvalidLogLevel("Invalid level expected value from 0 to 4 received {level} instead.")
            

    def __call__(self):
        self.add_handler()

if __name__ == "__main__":
    logger = Logger(name=__file__, handler_type='stream', log_level='debug')
    logger()
    logger.log(0, "This is a debug log")
        

    
    



