"""核心模块"""

from PySide6.QtCore import QDate, QDateTime, QObject, QRect, QSize, QTimer

from Gui.Calendar import CalendarWidget
from Gui.Modules import CntDayWnd, CourseShdWnd, DailyShdWnd, TimeWnd
from Gui.RemindWnd import RemindWnd
from Model import CountdayItem, DataSource
from Utils import Config, logger

Duration = 180  # 提前提醒时间，单位为秒


class MainModule( QObject ):
    """主模块"""
    
    def __init__( self, screenRect: QRect, parent = None ):
        super().__init__( parent )
        
        self.dataSource = DataSource()  # 数据源
        self.dataSource.loadDataFromDatabase()
        
        self.timeWnd = TimeWnd()  # 时间窗口
        self.timeWnd.setFixedSize( QSize( 140, 60 ) )
        textColor = Config.getValue( "colors", "timerTextColor" )
        if textColor is not None:
            self.timeWnd.setTextColor( textColor )
        
        self.dailyWnd = DailyShdWnd( self.dataSource.getDailyShdItem() )  # 作息窗口
        self.dailyWnd.setFixedSize( QSize( 140, 80 ) )
        textColor = Config.getValue( "colors", "dailyTextColor" )
        if textColor is not None:
            self.dailyWnd.setTextColor( textColor )
        
        self.courseWnd = CourseShdWnd( self.dataSource.getCourseShdItem() )  # 课程窗口
        self.courseWnd.setFixedSize( QSize( 140, 80 ) )
        textColor = Config.getValue( "colors", "courseTextColor" )
        if textColor is not None:
            self.courseWnd.setTextColor( textColor )
        
        self.calendarWnd = CalendarWidget()  # 日历窗口
        self.calendarWnd.setFixedSize( QSize( 140, 140 ) )
        # 从配置文件中读取颜色信息
        textColor = Config.getValue( "colors", "calendartextcolor" )
        if textColor is not None:
            self.calendarWnd.setColor( textColor )
        
        self.countDays: list[CntDayWnd] = list()  # 倒数日窗口
        self.cntDayInit()
        
        self.remindWnd = RemindWnd()  # 提醒窗口
        self.remindWnd.setFixedSize( QSize( 200, 100 ) )
        
        self.layoutAllWnd( screenRect )
        
        self.currentDate: QDate = QDate.currentDate()  # 当前日期
        self.dailyCheckTime: QDateTime = self.dailyWnd.dailyShd.end  # 作息检查时间
        self.CourseCheckTime: QDateTime = self.courseWnd.courseShd.end  # 课程检查时间
        self.remindTime: QDateTime = self.courseWnd.courseShd.start.addSecs(
            -Duration,
        )  # 提醒时间
        
        self.updateAllWnd()
        
        self.timer = QTimer( self )
        self.timer.timeout.connect( self.updateAllWnd )
        self.timer.start( 200 )  # 200ms
    
    def showAllWnd( self ):
        """显示所有窗口"""
        self.timeWnd.show()
        self.dailyWnd.show()
        self.courseWnd.show()
        self.calendarWnd.show()
        for cntDayWnd in self.countDays:
            cntDayWnd.show()
    
    def updateAllWnd( self ):
        """分级更新所有窗口"""
        curDateTime = QDateTime.currentDateTime()
        self.timeWnd.update( curDateTime )
        
        if curDateTime >= self.dailyCheckTime:  # 检查是否需要更新作息
            if self.dailyWnd.isExpired( curDateTime ):
                self.dailyWnd.setDailyShd( self.dataSource.getDailyShdItem() )
                self.dailyWnd.update()
                if self.dailyWnd.dailyShd is not None:  # 更新检查时间
                    self.dailyCheckTime = self.dailyWnd.dailyShd.end
                else:
                    self.dailyCheckTime = curDateTime.addSecs( 60 )
        
        if curDateTime >= self.CourseCheckTime:  # 检查是否需要更新课程
            if self.courseWnd.isExpired( curDateTime ):
                self.courseWnd.setCourseShd( self.dataSource.getCourseShdItem() )
                self.courseWnd.update()
                if self.courseWnd.courseShd is not None:
                    self.CourseCheckTime = self.courseWnd.courseShd.end  # 更新检查时间
                    self.remindTime = self.courseWnd.courseShd.start.addSecs( -Duration )
                else:
                    self.CourseCheckTime = curDateTime.addSecs( 60 )
        
        if self.currentDate != curDateTime.date():  # 检查是否需要更新日历和倒数日
            self.currentDate = curDateTime.date()
            self.calendarWnd.updateCalendar()
            for cntDayWnd in self.countDays:
                cntDayWnd.update()
        
        if (
                self.remindTime is not None and curDateTime >= self.remindTime
        ):  # 检查是否需要提醒
            self.remindTime = None  # 重置提醒时间
            self.remindWnd.remindStart( self.courseWnd.courseShd.start )
    
    def cntDayInit( self ):
        """初始化倒数日窗口"""
        schedule = self.dataSource.getCountdaySchedule()
        item: CountdayItem
        for item in schedule:
            cntDayWnd = CntDayWnd( item )
            cntDayWnd.setFixedSize( QSize( 140, 40 ) )
            self.countDays.append( cntDayWnd )
            textColor = Config.getValue( "colors", f"{item.text}" )
            if textColor is not None:
                cntDayWnd.setTextColor( textColor )
    
    def closeAllWnd( self ):
        """关闭所有窗口"""
        self.timeWnd.close()
        self.dailyWnd.close()
        self.courseWnd.close()
        self.calendarWnd.close()
        for cntDayWnd in self.countDays:
            cntDayWnd.close()
        logger.info( f"程序退出" )
    
    def layoutAllWnd( self, screenRect: QRect ):
        """布局所有窗口"""
        firstRun = Config.getValue( "condition", "firstrun" )
        if firstRun is None or firstRun == "True":
            self.defaultWndPos( screenRect )
            Config.setValue( "condition", "firstrun", "False" )
        else:
            self.moveWndPos()
    
    def moveWndPos( self ):
        """移动窗口位置"""
        
        def movePos( wnd, posKey ):
            posString = Config.getValue( "wndposition", posKey )
            x, y = list( map( int, posString.split( "," ) ) )
            wnd.move( x, y )
        
        wnds = [
            self.timeWnd,
            self.dailyWnd,
            self.calendarWnd,
            self.courseWnd,
        ]
        wnds.extend( self.countDays )
        
        keys = [
            "timeWndPos",
            "dailyShdWndPos",
            "calendarWidgetPos",
            "courseShdWndPos",
        ]
        keys.extend( [f"{wnd.countDay.text}" for wnd in self.countDays] )
        
        for wnd, key in zip( wnds, keys ):
            movePos( wnd, key )
    
    def defaultWndPos( self, screenRect: QRect ):
        """设置默认窗口位置"""
        space = 4
        left = screenRect.width() - 160
        top = 10
        
        self.timeWnd.move( left, top )
        Config.setValue( "wndposition", "timeWndPos", f"{left},{top}" )
        top += self.timeWnd.height() + space
        
        self.dailyWnd.move( left, top )
        Config.setValue( "wndposition", "dailyShdWndPos", f"{left},{top}" )
        top += self.dailyWnd.height() + space
        
        self.calendarWnd.move( left, top )
        Config.setValue( "wndposition", "calendarWidgetPos", f"{left},{top}" )
        top += self.calendarWnd.height() + space
        
        self.courseWnd.move( left, top )
        Config.setValue( "wndposition", "courseShdWndPos", f"{left},{top}" )
        top += self.courseWnd.height() + space
        
        for cntDayWnd in self.countDays:
            cntDayWnd.move( left, top )
            Config.setValue( "wndposition", f"{cntDayWnd.countDay.text}", f"{left},{top}" )
            top += cntDayWnd.height() + space
            if top >= screenRect.height():
                left -= 160
                top = 10
    
    def __del__( self ):
        """析构函数"""
        self.closeAllWnd()
        self.timer.stop()
