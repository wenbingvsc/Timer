"""模块测试"""

import sys

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication

from Gui import MainModule
from Utils import Config, logger, Paths, Screens


def main():
    """主函数"""
    app = QApplication( sys.argv )
    app.setQuitOnLastWindowClosed( True )  # 最后一个窗口关闭时退出应用程序
    Screens.getScreenInfo( app )
    
    logger.info( f"程序启动, 位置：{Paths.AppDir}" )
    if not Config.ready:
        logger.error( f"配置文件 {Config.configFile} 加载失败" )
        errors = Config.getErrorMsg()
        for error in errors:
            logger.error( f"{error}" )
    else:
        logger.info( f"配置文件 {Config.configFile} 加载成功" )
    
    screenRect: QRect = Screens.primeryScreen.geometry()  # 获取屏幕大小
    core = MainModule( screenRect )
    core.showAllWnd()
    
    sys.exit( app.exec() )


if __name__ == "__main__":
    main()
