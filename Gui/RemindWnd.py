"""创建倒计时窗口的类"""

import os

from PySide6.QtCore import QDateTime, QSize, Qt, QTimer, Slot
from winsound import PlaySound as playSound, SND_ASYNC, SND_FILENAME

from Gui.Widget.CLabelWnd import CLabelWnd
from Utils import Config, logger, Paths, Screens

SOUND_FILE = "Ring06.wav"
WinSize = QSize( 100, 80 )


class RemindWnd( CLabelWnd ):
    """
    倒计时窗口类
    """
    
    def __init__( self ):
        super().__init__()
        
        self.makeWindowStayOnTop()
        # 确保关闭窗口时不被销毁
        self.setAttribute( Qt.WidgetAttribute.WA_DeleteOnClose, False )
        self.setFixedSize( WinSize )
        self.createUI()
        self.colorChanged.connect( self.onColorChanged )
        self.alarmDateTime = None  # 初始化闹钟时间
        self.setTimer()
        self.filepath = os.path.join( Paths.MediaDir, SOUND_FILE )  # 铃声文件
    
    def makeWindowStayOnTop( self ):
        """将窗口置顶"""
        # 获取当前窗口标志
        current_flags = self.windowFlags()
        # 添加 Qt.WindowType.WindowStaysOnTopHint 标志
        new_flags = current_flags | Qt.WindowType.WindowStaysOnTopHint
        # 设置新的窗口标志
        self.setWindowFlags( new_flags )
    
    def setWndPos( self ):
        """设置窗口初始位置"""
        screen = Screens.primeryScreen
        screenGeometry = screen.availableGeometry()
        screenWidth = screenGeometry.width()
        screenHeight = screenGeometry.height()
        self.move(
            int( (screenWidth - WinSize.width()) / 2 ),
            int( screenHeight * 0.05 ),
        )
    
    def setTimer( self ):
        """设置计时器"""
        self.timer = QTimer( self )
        self.timer.timeout.connect( self.updateTimer )
    
    def remindStart( self, alarmDateTime: QDateTime = None ):
        """启动计时器"""
        if self.timer.isActive() and self.isVisible():
            return
        logger.info( f"启动提醒: {alarmDateTime}" )
        self.alarmDateTime = alarmDateTime
        playSound( self.filepath, SND_FILENAME | SND_ASYNC )
        self.updateTimer()
        self.timer.start( 200 )  # 每200毫秒更新一次
        self.show()
    
    def updateTimer( self ):
        """更新计时器"""
        
        currentDateTime = QDateTime.currentDateTime()
        
        if self.alarmDateTime is None:
            self.timer.stop()
            self.alarmDateTime = None
            self.close()  # 关闭窗口
            return
        
        if self.alarmDateTime <= currentDateTime:
            self.timer.stop()
            self.alarmDateTime = None
            self.close()  # 关闭窗口
            return
        
        restDuration = currentDateTime.secsTo( self.alarmDateTime )
        
        self.setText( self.formatRestDuration( restDuration ) )
    
    @staticmethod
    def formatRestDuration( restDuration: int ):
        """格式化剩余时间"""
        hours = int( restDuration // 3600 )
        minutes = int( (restDuration % 3600) // 60 )
        seconds = int( restDuration % 60 )
        formattedTime = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return formattedTime
    
    def createUI( self ):
        """创建UI"""
        self.setSampleStr( "000:00:00" )  # 设置示例文本
        self.setTextColor( "#cc3322" )
        self.setWndPos()
    
    @Slot( str )
    def onColorChanged( self, color ):
        """
        处理颜色改变事件
        :param color: 新的颜色
        """
        Config.setValue( "colors", "remindertextcolor", color )
