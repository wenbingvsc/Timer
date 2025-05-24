"""工具类模块"""

from .ConfigInfo import ConfigManager
from .logrecorder import LogRecorder
from .pathUtils import PathUtils
from .ScreenInfo import Screen

# 路径工具类实例
Paths = PathUtils()

# 配置管理器实例
Config = ConfigManager( Paths.ConfigFile )

# 屏幕工具类实例
Screens = Screen()

# 日志记录器
logger = LogRecorder( "Timer", Paths.LogDir ).getLogger()  # 获取日志记录器

__all__ = [
    "Paths",
    "Screens",
    "logger",
    "Config",
]
