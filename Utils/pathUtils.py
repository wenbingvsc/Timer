"""路径处理相关工具函数"""

import os
import winreg


def getDesktopDir( errorReceiver: list[str] ) -> str | None:
    """通过注册表获取windows桌面路径"""
    try:
        # 打开注册表项
        reg_subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        key = winreg.OpenKey( winreg.HKEY_CURRENT_USER, reg_subkey )
        # 获取桌面路径
        desktop_path, _ = winreg.QueryValueEx( key, "Desktop" )
        expanded_path = os.path.expandvars(
            desktop_path,
        )  # 使用 os.path.expandvars 展开路径中的环境变量
        # 关闭注册表项
        winreg.CloseKey( key )
        return expanded_path
    except Exception as e:
        errorReceiver.append( f"获取桌面路径时出错: {e}" )
        return None


def getApplDir() -> str:
    """获取App文件路径"""
    filepath: str = os.path.dirname( os.path.abspath( __file__ ) )
    filepath = filepath.replace( r"\_internal", "" )
    filepath = os.path.dirname( filepath )
    return filepath


class PathUtils:
    """路径处理工具类"""
    
    def __init__( self ):
        self.__errors: list[str] = list()
        self.__desktopDir = getDesktopDir( self.__errors )  # 获取Windows桌面的路径
        self.__appDir = getApplDir()  # 获取应用程序的路径
        
        if self.__desktopDir is None:
            self.__outputDir = os.path.join( self.__appDir, "Output" )  # 输出文件的路径
        else:
            self.__outputDir = os.path.join( self.__desktopDir, "Output" )  # 输出文件的路径
        
        self.__logDir = os.path.join( self.__appDir, "log" )  # 日志文件的路径
        self.__databasePath = os.path.join( self.__appDir, "database.sqlite3" )  # 数据库文件的路径
        self.__mediaDir = os.path.join( self.__appDir, "media" )  # 媒体文件的路径
        
        self.__configPath = os.path.join( self.__appDir, "config.ini" )  # 配置文件的路径
        
        if not os.path.exists( self.__outputDir ):
            os.mkdir( self.__outputDir )
        if not os.path.exists( self.__logDir ):
            os.mkdir( self.__logDir )
    
    @property
    def DesktopDir( self ):
        return self.__desktopDir
    
    @property
    def AppDir( self ):
        return self.__appDir
    
    @AppDir.setter
    def AppDir( self, dirString: str ):
        self.__appDir = dirString
    
    @property
    def OutputDir( self ):
        return self.__outputDir
    
    @property
    def LogDir( self ):
        return self.__logDir
    
    @property
    def DatabaseFile( self ):
        return self.__databasePath
    
    @property
    def MediaDir( self ):
        return self.__mediaDir
    
    @property
    def ConfigFile( self ):
        return self.__configPath
