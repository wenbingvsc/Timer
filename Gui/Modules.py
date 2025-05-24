"""Application Modules"""

from PySide6.QtCore import QDate, QDateTime, QPoint, QTimer, Slot
from PySide6.QtGui import QMouseEvent

from Gui.configwnd import ConfigDialog
from Gui.CourseWnd import CourseEditWnd
from Gui.Widget import CLabelWnd
from Model import CountdayItem, CourseShdItem, DailyShdItem
from Utils import Config, logger


class TimeWnd( CLabelWnd ):
    """Time Window"""
    
    def __init__( self ):
        super().__init__()
        self.posMoved.connect( self.onPosMoved )
        self.colorChanged.connect( self.onColorChanged )
        self.update = lambda curDateTime: self.setText( curDateTime.toString( "hh:mm:ss" ) )
        self.setSampleStr( "000:00:00" )
    
    @Slot( QPoint )
    def onPosMoved( self, pos ):
        """
        处理窗口位置移动事件
        :param pos: 窗口新的位置
        """
        Config.setValue( "wndposition", "timeWndPos", f"{pos.x()},{pos.y()}" )
    
    @Slot( str )
    def onColorChanged( self, color ):
        """
        处理颜色改变事件
        :param color: 新的颜色
        """
        Config.setValue( "colors", "timertextcolor", color )


class CntDayWnd( CLabelWnd ):
    """Count Day Window"""
    
    def __init__( self, countDay: CountdayItem ):
        super().__init__()
        self.posMoved.connect( self.onPosMoved )
        self.colorChanged.connect( self.onColorChanged )
        self.countDay: CountdayItem = countDay
        self.setSampleStr( "距国庆节365天" )
        self.update()
    
    def update( self ):
        """Update the text"""
        if self.countDay is None:
            self.setText( "None" )
            logger.info( "当前没有倒数日项目" )
        else:
            self.setText( self.countDay.screenText() )
            logger.info( f"更新倒数日: {self.countDay}" )
    
    def setCountDay( self, countDay: CountdayItem ):
        """Set Count Day"""
        self.countDay = countDay
        self.update()
    
    def isExpired( self, curDate: QDate ) -> bool:
        """Check if the schedule is expired"""
        if self.countDay is None:
            return True
        return self.countDay.isExpired( curDate )
    
    def mouseDoubleClickEvent( self, event: QMouseEvent ):
        """
        处理鼠标双击事件
        :param event: 鼠标事件对象
        """
        QTimer.singleShot( 500, self.openConfigWnd )
        event.accept()
    
    def openConfigWnd( self ):
        """打开配置窗口"""
        try:
            logger.info( "打开配置窗口" )
            dlg = ConfigDialog( self )
            dlg.exec()
        except Exception as e:
            logger.error( f"打开课程表窗口时出错: {e}" )
    
    @Slot( QPoint )
    def onPosMoved( self, pos ):
        """
        处理窗口位置移动事件
        :param pos: 窗口新的位置
        """
        Config.setValue( "wndposition", f"{self.countDay.text}", f"{pos.x()},{pos.y()}" )
    
    @Slot( str )
    def onColorChanged( self, color ):
        """
        处理颜色改变事件
        :param color: 新的颜色
        """
        Config.setValue( "colors", f"{self.countDay.text}", color )


class DailyShdWnd( CLabelWnd ):
    """Daily schedule Window"""
    
    def __init__( self, dailyShd: DailyShdItem ):
        super().__init__()
        self.posMoved.connect( self.onPosMoved )
        self.colorChanged.connect( self.onColorChanged )
        self.dailyShd: DailyShdItem = dailyShd
        self.setSampleStr( "00:00 - 08:00\n课间休息" )
        self.update()
    
    def update( self ):
        """Update the text"""
        if self.dailyShd is None:
            self.setText( "None" )
            logger.info( "当前没有作息项目" )
        else:
            self.setText( self.dailyShd.screenText() )
            logger.info( f"更新作息: {self.dailyShd}" )
    
    def setDailyShd( self, dailyShd: DailyShdItem ):
        """Set Daily schedule"""
        self.dailyShd = dailyShd
        # self.update()
    
    def isExpired( self, curDateTime: QDateTime ) -> bool:
        """Check if the schedule is expired"""
        if self.dailyShd is None:
            return True
        return self.dailyShd.isExpired( curDateTime )
    
    def mouseDoubleClickEvent( self, event: QMouseEvent ):
        """
        处理鼠标双击事件
        :param event: 鼠标事件对象
        """
        QTimer.singleShot( 200, self.openConfigWnd )
        event.accept()
    
    def openConfigWnd( self ):
        """打开配置窗口"""
        try:
            logger.info( "打开配置窗口" )
            dlg = ConfigDialog( self )
            dlg.exec()
        except Exception as e:
            logger.error( f"打开课程表窗口时出错: {e}" )
    
    @Slot( QPoint )
    def onPosMoved( self, pos ):
        """
        处理窗口位置移动事件
        :param pos: 窗口新的位置
        """
        Config.setValue( "wndposition", "dailyShdWndPos", f"{pos.x()},{pos.y()}" )
    
    @Slot( str )
    def onColorChanged( self, color ):
        """
        处理颜色改变事件
        :param color: 新的颜色
        """
        Config.setValue( "colors", "dailytextcolor", color )


class CourseShdWnd( CLabelWnd ):
    """Course schedule Window"""
    
    def __init__( self, courseShd: CourseShdItem ):
        super().__init__()
        self.posMoved.connect( self.onPosMoved )
        self.colorChanged.connect( self.onColorChanged )
        self.courseShd: CourseShdItem = courseShd
        self.setSampleStr( "星期一 上午第一节\n00:00 - 08:00\n高一13班物理" )
        self.update()
    
    def update( self ):
        """Update the text"""
        if self.courseShd is None:
            self.setText( "None" )
            logger.info( "当前没有课程项目" )
        else:
            self.setText( self.courseShd.screenText() )
            logger.info( f"更新课程: {self.courseShd}" )
    
    def setCourseShd( self, courseShd: CourseShdItem ):
        """Set Course schedule"""
        self.courseShd = courseShd
        # self.update()
    
    def isExpired( self, curDateTime: QDateTime ) -> bool:
        """Check if the schedule is expired"""
        if self.courseShd is None:
            return True
        return self.courseShd.isExpired( curDateTime )
    
    def mouseDoubleClickEvent( self, event: QMouseEvent ):
        """
        处理鼠标双击事件
        :param event: 鼠标事件对象
        """
        QTimer.singleShot( 200, self.openCourseShdWnd )
        event.accept()
    
    def openCourseShdWnd( self ):
        """打开课程表窗口"""
        try:
            logger.info( "打开课程表窗口" )
            dlg = CourseEditWnd( self )
            dlg.exec()
        except Exception as e:
            logger.error( f"打开课程表窗口时出错: {e}" )
    
    @Slot( QPoint )
    def onPosMoved( self, pos ):
        """
        处理窗口位置移动事件
        :param pos: 窗口新的位置
        """
        Config.setValue( "wndposition", "CourseShdWndPos", f"{pos.x()},{pos.y()}" )
    
    @Slot( str )
    def onColorChanged( self, color ):
        """
        处理颜色改变事件
        :param color: 新的颜色
        """
        Config.setValue( "colors", "coursetextcolor", color )
