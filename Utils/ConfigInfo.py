"""配置文件读写模块"""

import configparser  # Python 标准库中的一个模块，用于读取和写入配置文件

"""
1. 创建 ConfigParser 解析器对象。
self.__configer = configparser.ConfigParser():
这个对象用于读取和写入配置文件。

2. 读取配置文件
self.__configer.read():
读取并解析一个文件名或者一个文件名的列表。
无法打开的文件会被自动忽略；这样设计的目的是让您能够指定一系列可能的配置文件
位置（例如当前目录、用户的主目录、系统范围的目录），并且该范围内所有的现有配置
文件都会被读取。也可以只给出一个文件名。
返回已成功读取的文件列表

3.DEFAULT 部分是配置文件里一个特殊的节，它能为所有其他节提供默认值。
sections() 方法的设计目的是返回配置文件里显式定义的节，不包含 DEFAULT 部分。
不过，在读取其他节的键值时，若该节没有对应的键，就会从 DEFAULT 部分查找。
"""


class ConfigManager:
    def __init__( self, configFile ):
        self.configFile: str = configFile
        self.__parser = configparser.ConfigParser()  # 创建 ConfigParser 解析器对象
        self.__ready: bool = False
        self.__errorMsg: list = []
        self.__readConfig()
    
    def __readConfig( self ):
        """读取配置文件"""
        try:
            readFiles = self.__parser.read( self.configFile, encoding = 'utf-8' )
            if readFiles:
                self.__ready = True
            else:
                self.__ready = False
                self.__errorMsg.append( f'配置文件 {self.configFile} 不存在或无法读取' )
        except Exception as e:
            self.__ready = False
            self.__errorMsg.append( f'配置文件 {self.configFile} 读取失败: {e}' )
    
    @property
    def ready( self ):
        """检查配置文件是否成功读取"""
        return self.__ready
    
    def getErrorMsg( self ):
        """
        获取错误信息
        :return: 错误信息列表
        """
        msg = self.__errorMsg.copy()
        self.__errorMsg.clear()
        return msg
    
    def getSection( self, section ):
        """
        获取指定的配置项
        :param section: 配置项所在的节
        :return: 配置项的字典，如果配置项不存在则返回 None
        """
        if not self.ready:
            return None
        if self.__parser.has_section( section ):
            return self.__parser[section]
        else:
            return None
    
    def getValue( self, section, key ):
        """
        获取指定的配置项的值
        :param section: 配置项所在的节
        :param key: 配置项的键
        :return: 配置项的值，如果配置项不存在则返回 None
        """
        if not self.ready:
            return None
        if self.__parser.has_section( section ):
            if self.__parser.has_option( section, key ):
                return self.__parser.get( section, key )
            else:
                return None
        else:
            return None
    
    def setValue( self, section, key, value ):
        """
        设置指定的配置项的值
        :param section: 配置项所在的节
        :param key: 配置项的键
        :param value: 配置项的值
        :return: 如果设置成功则返回 True，否则返回 False
        """
        if not self.ready:
            return False
        if not self.__parser.has_section( section ):
            self.__parser.add_section( section )
        self.__parser.set( section, key, value )
        try:
            with open( self.configFile, 'w', encoding = 'utf-8' ) as configfile:
                self.__parser.write( configfile )
            return True
        except Exception as e:
            self.__errorMsg.append( f'配置文件 {self.configFile} 写入失败: {e}' )
            return False
