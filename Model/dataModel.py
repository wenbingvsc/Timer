"""data model"""

from PySide6.QtCore import QDate, QDateTime, QObject, Signal
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

from Model.Norm import (
    checkDateString,
    checkPeriodString,
    checkTimeString,
    checkWeekdayString,
    formatDateString,
    formatTimeString,
    Weekday,
)
from Utils import logger, Paths


class DailyShdItem:
    """
    dailyScheduleItem
    作息表项，包含开始时间,结束时间,时间段：
        时间段格式为: 上午第1节, 下午第2节, 晚上第3节, 课间休息, 下班, 午休, 晚饭时间, 休息时间, 体育锻炼
        时间格式为: hh:mm
    """
    
    def __init__(
            self,
            start: QDateTime = None,
            end: QDateTime = None,
            period: str = "",
    ):
        self.start: QDateTime = start
        self.end: QDateTime = end
        self.period: str = period
    
    def isValid( self ):
        """数据规范性"""
        if self.start is None or self.end is None:
            return False
        if not self.start.isValid() or not self.end.isValid():
            return False
        return checkPeriodString( self.period )
    
    def isThis( self, dateTime: QDateTime ):
        """检测指定时间是否在本时间段内"""
        return self.start <= dateTime < self.end
    
    def isBefore( self, dateTime: QDateTime ):
        """检测本时间段是否在指定时间之前"""
        return self.end <= dateTime
    
    def isExpired( self, dateTime: QDateTime ):
        """检测本时间段是否已过期"""
        return self.end <= dateTime
    
    def getTime( self ):
        """获取时间"""
        return self.start, self.end
    
    def setNextday( self ):
        """将当前Item修改为下一天"""
        self.start = self.start.addDays( 1 )
        self.end = self.end.addDays( 1 )
    
    def screenText( self ):
        """获取文本"""
        return (
            f"{self.start.toString( 'hh:mm' )} - "
            f"{self.end.toString( 'hh:mm' )}\n{self.period}"
        )
    
    def __str__( self ):
        """获取文本"""
        return (
            f"{self.start.toString( 'yyyy-MM-dd hh:mm' )} - "
            f"{self.end.toString( 'yyyy-MM-dd hh:mm' )} {self.period}"
        )


class DailySchedule:
    """
    作息时间表,过时的项会被修改为后一天对应项
    """
    
    def __init__( self, schedule: list[DailyShdItem] = None ):
        self.schedule: list[DailyShdItem] = schedule if schedule is not None else list()
    
    def addItem( self, scheduleItem: DailyShdItem ):
        """添加"""
        if scheduleItem.isValid():
            self.schedule.append( scheduleItem )
        else:
            logger.warning( f"作息表添加失败: {scheduleItem}" )
    
    def getCurrentItem( self ) -> DailyShdItem | None:
        """获取当前时间项，如果当前时间不在任何时间段内，则返回None"""
        if len( self.schedule ) == 0:
            logger.warning( "作息表为空" )
            return None
        self.schedule.sort( key = lambda x: x.start )  # 按start排序
        currentDateTime = QDateTime.currentDateTime()  # 当前时间
        for item in self.schedule:
            if item.isThis( currentDateTime ):
                return item
            elif item.isExpired( currentDateTime ):
                item.setNextday()
        else:
            return None
    
    def findItemByPeriod( self, period: str ) -> DailyShdItem | None:
        """根据period查找对应的时间项"""
        for item in self.schedule:
            if item.period == period:
                return item
        else:
            return None
    
    def loadDailySchedule( self, model: QSqlTableModel ):
        """
        从数据库加载作息时间表
        """
        if model is None:
            logger.warning( "数据库模型为空: None" )
            return
        self.schedule.clear()  # 清空当前列表
        currentDate = QDate.currentDate().toString( "yyyy-MM-dd" )
        
        rowCount = model.rowCount()
        for row in range( rowCount ):
            
            start = formatTimeString( model.record( row ).value( "start_time" ) )
            end = formatTimeString( model.record( row ).value( "end_time" ) )
            period = model.record( row ).value( "period" )
            
            if (
                    checkTimeString( start )
                    and checkTimeString( end )
                    and checkPeriodString( period )
            ):
                startDateTime = QDateTime.fromString(
                    f"{currentDate} {start}",
                    "yyyy-MM-dd hh:mm",
                )
                endDateTime = QDateTime.fromString(
                    f"{currentDate} {end}",
                    "yyyy-MM-dd hh:mm",
                )
                
                self.addItem(
                    DailyShdItem( startDateTime, endDateTime, period ),
                )
            else:
                logger.warning(
                    f"作息表加载失败，第{row}行数据格式错误: {start} - {end} {period}",
                )
        
        if len( self.schedule ) > 0:
            self.schedule.sort( key = lambda x: x.start )  # 按start排序
        
        logger.info( f"作息表加载完成，加载{len( self.schedule )}条记录" )


class CourseShdItem:
    """
    课程表条目，包含开始时间,结束时间,星期,时间段,课程名称
    星期格式为: 星期一, 星期二, 星期三, 星期四, 星期五, 星期六, 星期日
    时间段格式为: 上午第1节, 下午第2节, 晚上第3节
    """
    
    def __init__(
            self,
            start: QDateTime = None,
            end: QDateTime = None,
            weekday: str = "",
            period: str = "",
            subject: str = "",
    ):
        self.start: QDateTime = start
        self.end: QDateTime = end
        self.subject: str = subject
        self.period: str = period
        self.weekday: str = weekday
    
    def isValid( self ):
        """数据规范性"""
        if self.start is None or self.end is None:
            return False
        if not self.start.isValid() or not self.end.isValid():
            return False
        return True
    
    def isThis( self, dateTime: QDateTime ):
        """检测指定时间是否在本课程时间段内"""
        return self.start <= dateTime < self.end
    
    def isBefore( self, dateTime: QDateTime ):
        """检测本课程时间段是否在指定时间之前"""
        return self.end < dateTime
    
    def isExpired( self, dateTime: QDateTime ):
        """检测本课程时间段是否已过期"""
        return self.end <= dateTime
    
    def setNextWeekday( self ):
        """将当前Item修改为下一周"""
        self.start = self.start.addDays( 7 )
        self.end = self.end.addDays( 7 )
    
    def __str__( self ):
        """获取文本"""
        return (
            f"{self.start.toString( 'yyyy-MM-dd hh:mm' )} - "
            f"{self.end.toString( 'yyyy-MM-dd hh:mm' )} "
            f"{self.weekday} {self.period} {self.subject}"
        )
    
    def screenText( self ):
        """获取文本"""
        return (
            f"{self.weekday} {self.period}\n{self.start.toString( 'hh:mm' )} - "
            f"{self.end.toString( 'hh:mm' )}\n{self.subject}"
        )


class CourseSchedule:
    """课程表"""
    
    def __init__( self, schedule: list[CourseShdItem] = None ):
        self.schedule: list[CourseShdItem] = (
            schedule if schedule is not None else list()
        )
    
    def addItem( self, scheduleItem: CourseShdItem ):
        """添加课表项"""
        if scheduleItem.isValid():
            self.schedule.append( scheduleItem )
        else:
            logger.warning( f"课程表项添加失败: {scheduleItem}" )
    
    def getCurrentItem( self ) -> CourseShdItem | None:
        """获取当前时间对应的课表项，如果没有，则返回当前时间对应的后一个课表项"""
        if len( self.schedule ) == 0:
            logger.warning( "课程表为空" )
            return None
        self.schedule.sort( key = lambda x: x.start )
        currentDateTime = QDateTime.currentDateTime()
        for item in self.schedule:
            if item.isExpired( currentDateTime ):
                item.setNextWeekday()
            else:
                return item
        else:
            # 当前课表项都过期,已经全部被设置为后一周对应课表项,返回第一个
            return self.schedule[0]
    
    def loadCourseSchedule( self, model: QSqlTableModel, dailySchedule: DailySchedule ):
        """从数据库加载课程表"""
        if dailySchedule is None or model is None:
            logger.warning( "作息表或数据库模型为空: None" )
            return
        self.schedule.clear()  # 清空当前列表
        weekday_list = Weekday.CWEEKDAYS  # 星期列表
        
        # 当前日期
        currentDate = QDate.currentDate()
        currentWeekdayIndex = currentDate.dayOfWeek() - 1
        
        rowCount = model.rowCount()
        for row in range( rowCount ):
            
            # 计算日期
            weekday = model.record( row ).value( "weekday" )
            if not checkWeekdayString( weekday ):
                logger.warning( f"第{row}行星期格式错误: {weekday}" )
                continue
            weekdayIndex = weekday_list.index( weekday )
            date = currentDate.addDays( weekdayIndex - currentWeekdayIndex )
            
            # 计算开始时间和结束时间
            period = model.record( row ).value( "period" )
            if not checkPeriodString( period ):
                logger.warning( f"第{row}行时间段格式错误: {period}" )
                continue
            dailyScheduleItem = dailySchedule.findItemByPeriod(
                period,
            )  # 查找对应的作息表项
            if dailyScheduleItem is None:
                logger.warning( f"第{row}行时间段不存在: {period}" )
                continue
            start, end = dailyScheduleItem.getTime()
            startDateTime = QDateTime.fromString(
                f"{date.toString( 'yyyy-MM-dd' )} {start.toString( 'hh:mm' )}",
                "yyyy-MM-dd hh:mm",
            )
            endDateTime = QDateTime.fromString(
                f"{date.toString( 'yyyy-MM-dd' )} {end.toString( 'hh:mm' )}",
                "yyyy-MM-dd hh:mm",
            )
            
            subject = model.record( row ).value( "course" )
            
            # 添加课程表条目
            self.addItem(
                CourseShdItem(
                    startDateTime,
                    endDateTime,
                    weekday,
                    period,
                    subject,
                ),
            )
        
        if len( self.schedule ) > 0:
            self.schedule.sort( key = lambda x: x.start )
        logger.info( f"课程表加载完成, 加载{len( self.schedule )}条记录" )


class CountdayItem:
    """倒数日条目"""
    
    def __init__( self, date: QDate = None, text: str = "" ):
        self.date: QDate = date
        self.text: str = text
    
    def __str__( self ):
        """获取文本"""
        return f"{self.date.toString( 'yyyy-MM-dd' )} {self.text}"
    
    def isValid( self ):
        """数据规范性"""
        if self.date is None:
            return False
        if not self.date.isValid():
            return False
        if len( self.text ) == 0:
            return False
        return True
    
    def screenText( self, currentDate: QDate = None ):
        """获取文本"""
        if currentDate is None:
            currentDate = QDate.currentDate()
        return f"距{self.text}{currentDate.daysTo( self.date )}天"
    
    def isExpired( self, currentDate: QDate ):
        """检测本条目是否已过期"""
        return self.date < currentDate


class CountdaySchedule:
    """倒数日表"""
    
    def __init__( self, schedule: list[CountdayItem] = None ):
        self.schedule: list[CountdayItem] = schedule if schedule is not None else list()
        self._index = 0  # 迭代器索引
    
    def addItem( self, scheduleItem: CountdayItem ):
        """添加"""
        if scheduleItem.isValid():
            self.schedule.append( scheduleItem )
        else:
            logger.warning( f"倒数日添加失败: {scheduleItem}" )
    
    def loadCountdaySchedule( self, model: QSqlTableModel ):
        """从数据库加载倒数日表"""
        if model is None:
            logger.warning( "数据库模型为空: None" )
            return
        self.schedule.clear()  # 清空当前列表
        currentDate = QDate.currentDate()
        rowCount = model.rowCount()
        for row in range( rowCount ):
            date = formatDateString( model.record( row ).value( "dateAndtime" ) )
            text = model.record( row ).value( "description" )
            if checkDateString( date ) and len( text ) > 0:
                countdayDate = QDate.fromString( date, "yyyy-MM-dd" )
                if countdayDate >= currentDate:
                    self.addItem( CountdayItem( countdayDate, text ) )
                else:
                    logger.warning( f"倒数日已经过期: {date} {text}" )
            else:
                logger.warning( f"倒数日加载失败, 第{row}行数据格式错误: {date} {text}" )
        self.schedule.sort( key = lambda x: x.date )
        logger.info( f"倒数日加载完成, 加载{len( self.schedule )}条记录" )
    
    # 实现 __iter__ 方法，返回迭代器对象
    # countday_schedule = CountdaySchedule()
    # for item in countday_schedule:
    #     print(item)
    def __iter__( self ):
        self._index = 0
        return self
    
    # 实现 __next__ 方法，返回下一个元素
    def __next__( self ):
        if self._index < len( self.schedule ):
            item = self.schedule[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration  # 抛出 StopIteration 异常，表示迭代结束


class DataSource( QObject ):
    """数据源"""
    
    dataIsReady = Signal()  # 数据加载完成信号
    
    def __init__( self ):
        super().__init__()
        self.dailySchedule = DailySchedule()
        self.courseSchedule = CourseSchedule()
        self.countdaySchedule = CountdaySchedule()
    
    def loadDataFromDatabase( self ):
        """从数据库加载数据"""
        db = connectToDb()
        if db is None:
            logger.error( "无法连接数据库" )
            return
        tableList = ["DailySchedule", "CourseSchedule", "params", "Countdown"]
        model = QSqlTableModel( self, db = db )  # 读取表数据
        
        # 作息表
        model.setTable( tableList[0] )
        model.select()
        self.dailySchedule.loadDailySchedule( model )
        
        # 课程表
        model.setTable( tableList[1] )
        model.select()
        self.courseSchedule.loadCourseSchedule( model, self.dailySchedule )
        
        # 倒数日
        model.setTable( tableList[3] )
        model.select()
        self.countdaySchedule.loadCountdaySchedule( model )
        
        logger.info( "数据加载完成" )
        self.dataIsReady.emit()  # 发送数据加载完成信号
        
        closeDb( db )
    
    def getDailyShdItem( self ) -> DailyShdItem | None:
        """获取当前时间对应的作息表项"""
        logger.info( "获取当前作息条目" )
        return self.dailySchedule.getCurrentItem()
    
    def getCourseShdItem( self ) -> CourseShdItem | None:
        """获取当前时间对应的课程表项，或者下一表项"""
        logger.info( "获取当前课程条目" )
        return self.courseSchedule.getCurrentItem()
    
    def getCountdaySchedule( self ):
        """获取倒数日表"""
        logger.info( "获取倒数日表" )
        return self.countdaySchedule


def connectToDb() -> QSqlDatabase | None:
    """创建数据库连接"""
    ConnectionName = "timer_db_connection"
    if QSqlDatabase.contains( ConnectionName ):
        db = QSqlDatabase.database( ConnectionName )
    else:
        db = QSqlDatabase.addDatabase( "QSQLITE", ConnectionName )
    db.setDatabaseName( Paths.DatabaseFile )
    if not db.open():
        logger.error( "无法打开数据库" )
        return None
    logger.info( "数据库连接成功" )
    return db


def closeDb( db: QSqlDatabase ):
    """关闭数据库连接"""
    if db is not None:
        db.close()
        logger.info( "数据库连接关闭" )


def createDbTable( db: QSqlDatabase, tableName: str, columns: list ) -> bool:
    """
    创建数据表
    :param db: 数据库连接对象
    :param tableName: 要创建的数据表名
    :param columns: 数据表的列定义列表，例如 ["start_time TEXT", "end_time TEXT", "period TEXT"]
    """
    if db is None:
        return False
    logger.info( f"创建表: {tableName}" )
    query = QSqlQuery( db )
    columnsString = ", ".join( columns )
    queryString = f"CREATE TABLE IF NOT EXISTS {tableName} ({columnsString})"
    return query.exec( queryString )
