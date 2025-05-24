"""
logging 模块是 Python 标准库的一部分, 它提供了灵活的日志记录功能, 可用于记录程序运行时的信息, 方便调试、监控和错误排查。
logging 模块提供了以下主要功能:
日志级别:logging 模块定义了不同的日志级别, 如 DEBUG、INFO、WARNING、ERROR 和 CRITICAL, 用于指示日志消息的重要性。
日志处理器:logging 模块提供了多种日志处理器, 如 StreamHandler、FileHandler、RotatingFileHandler、NullHandler、
            SocketHandler、DatagramHandler、SMTPHandler、SysLogHandler 等, 用于将日志消息输出到不同的目标, 如控制台、文件或网络。
日志格式化:logging 模块允许用户自定义日志消息的格式, 包括时间戳、日志级别、模块名、行号等信息。
日志配置:logging 模块提供了灵活的日志配置方式, 可以通过配置文件或编程方式来设置日志级别、处理器、格式化等参数。
日志记录:通过调用 logging 模块的函数, 可以在程序中记录日志消息, 如 logging.debug()、logging.info()、logging.warning() 等。
这些功能使得 logging 模块成为 Python 开发中常用的日志记录工具, 能够帮助开发者更好地理解和调试程序, 提高代码质量和可维护性。
"""

import logging
from logging.handlers import RotatingFileHandler


class LogRecorder:
    """
    日志记录器
    """

    def __init__(self, recorder: str, logPath: str, tostream: bool = False):
        """
        初始化日志记录器
        :param recorder: 日志记录器名称(日志来源）
        :param logPath: 日志文件路径(包括文件名)
        :param tostream: 是否输出到控制台,默认不输出到控制台
        """

        # 创建一个日志记录器
        self.__logger = logging.getLogger(recorder)
        self.__logger.setLevel(logging.DEBUG)

        # 滚动日志文件处理器,maxBytes: 文件大小达到该值时进行滚动, backupCount: 保留的旧文件数量
        fileHandler = RotatingFileHandler(
            logPath + "\\running.log",
            maxBytes=1024 * 1024 * 2,
            backupCount=10,
            encoding="utf-8",
        )
        fileHandler.setLevel(logging.DEBUG)

        # 创建一个格式化器，并将其添加到处理器中
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fileHandler.setFormatter(formatter)

        # 将处理器添加到日志记录器中
        self.__logger.addHandler(fileHandler)

        if tostream:  # 创建一个处理器，用于输出到控制台
            streamhandler = logging.StreamHandler()
            streamhandler.setLevel(logging.DEBUG)
            streamhandler.setFormatter(formatter)
            self.__logger.addHandler(streamhandler)

    def getLogger(self):
        """
        获取日志记录器
        :return: 日志记录器
        """
        return self.__logger
