"""创建课程表窗口"""

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QAbstractTableModel, QObject, Qt
from PySide6.QtGui import QCloseEvent, QColor
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QAbstractItemView, QApplication, QDialog, QTableView

from Gui.Style import SheetManager
from Model import (closeDb, connectToDb)
from Model.Norm import ClassPeriod, Weekday
from Utils import logger, Screens

dialogStyleSheet = """
    QDialog {
        background-color: #d0d0ff;
        border: 1px solid #dddddd;
        border-radius: 10px;
        padding: 10px;
    }
    """

ViewStyleSheet = """
                QTableView {
                    font-family: Arial;
                    font-size: 12px;
                    font-weight: 400;
                    color: #000000;
                    }
              """
HeadStyleSheet = """
         QHeaderView::section {
             font-family: Arial;
             font-size: 12px;
             font-weight: 400;
             color: #000000;
             border: 1px solid #dddddd;
             background-color: #f0f0f0;
         }
         """


class ScheduleItem:
    """课程表项"""
    
    def __init__(
            self,
            weekday: str = "",
            period: str = "",
            subject: str = "",
            modified: bool = False,
    ):
        """
        初始化课程表项
        :param weekday: 星期
        :param period: 节次
        :param subject: 课程
        :param modified: 是否修改
        """
        self.weekday: str = weekday
        self.period: str = period
        self.subject: str = subject
        self.modified: bool = modified
    
    def copyFrom( self, other ):
        """
        从其他课程表项复制数据
        :param other: 其他课程表项
        """
        self.weekday = other.weekday
        self.period = other.period
        self.subject = other.subject
        self.modified = other.modified
        return self
    
    def __copy__( self ):
        """
        复制课程表项
        :return: 复制后的课程表项
        """
        return ScheduleItem( self.weekday, self.period, self.subject, self.modified )
    
    def __eq__( self, other ):
        """
        比较两个课程表项是否相等
        :param other: 其他课程表项
        :return: 是否相等
        """
        return (
                self.weekday == other.weekday
                and self.period == other.period
                and self.subject == other.subject
                and self.modified == other.modified
        )
    
    def __str__( self ):
        """
        返回课程表项的字符串表示
        :return: 课程表项的字符串表示
        """
        return f"{self.weekday} {self.period} {self.subject}"
    
    def __repr__( self ):
        """
        返回课程表项的字符串表示
        :return: 课程表项的字符串表示
        """
        return f"ScheduleItem({self.weekday}, {self.period}, {self.subject}, {self.modified})"


class DatabaseManager( QObject ):
    """数据库管理器"""
    
    def __init__( self ):
        super().__init__()
        self.db = connectToDb()
        # 读取表数据
        if self.db is not None:
            self.model = QSqlTableModel( self, db = self.db )
            self.model.setTable( "CourseSchedule" )
            self.model.select()
            self.model.setEditStrategy( QSqlTableModel.EditStrategy.OnFieldChange )
            self.model.setHeaderData( 0, Qt.Orientation.Horizontal, "星期" )
            self.model.setHeaderData( 1, Qt.Orientation.Horizontal, "节次" )
            self.model.setHeaderData( 2, Qt.Orientation.Horizontal, "课程" )
        else:
            self.model = None
    
    def __del__( self ):
        if self.db is not None:
            closeDb( self.db )
    
    def __iter__( self ):
        self._index = 0
        return self
    
    # 实现 __next__ 方法，返回下一个元素
    def __next__( self ):
        if self.model is None:
            raise StopIteration
        if self._index < self.model.rowCount():
            weekday = self.model.record( self._index ).value( "weekday" )
            period = self.model.record( self._index ).value( "period" )
            subject = self.model.record( self._index ).value( "course" )
            self._index += 1
            return ScheduleItem( weekday, period, subject, False )
        else:
            raise StopIteration  # 抛出 StopIteration 异常，表示迭代结束


class CourseTableModel( QAbstractTableModel ):
    """课程表模型"""
    
    def __init__( self ):
        super().__init__()
        # 初始化课程数据，每周7天，每天9节课
        self.course_data = [[ScheduleItem() for _ in range( 7 )] for _ in range( 11 )]
        self.periods = ClassPeriod.CLASS_PERIODS  # 正课时段列表
        self.days = Weekday.CWEEKDAYS  # 星期列表
        self.dbMgr = DatabaseManager()  # 数据库管理器
        self.load_data()
    
    def load_data( self ):
        """从数据库加载课程数据"""
        for item in self.dbMgr:
            row = self.periods.index( item.period )
            col = self.days.index( item.weekday )
            self.course_data[row][col].copyFrom( item )
        logger.info( "课程表数据加载完毕" )
    
    def rowCount( self, parent = QtCore.QModelIndex() ):
        """返回行数，即11节可"""
        return 11
    
    def columnCount( self, parent = QtCore.QModelIndex() ):
        """返回列数，即7天"""
        return 7
    
    def data( self, index, role = Qt.ItemDataRole.DisplayRole ):
        """
        获取数据
        :param index:
        :param role:
        :return:
        """
        # role：Qt.ItemDataRole 类型的枚举值，用于指定要获取的数据类型
        # Qt.ItemDataRole.DisplayRole：该角色用于获取要在单元格中显示的文本数据
        if role == Qt.ItemDataRole.DisplayRole:
            return self.course_data[index.row()][index.column()].subject
        # Qt.ItemDataRole.BackgroundRole：该角色用于获取单元格的背景颜色
        elif role == Qt.ItemDataRole.BackgroundRole:
            row = index.row()
            if row < 4:  # 上午 4 节课
                return QColor( 255, 235, 205 )  # 浅橙色
            elif row < 8:  # 下午 4 节课
                return QColor( 244, 245, 200 )  # 浅黄色
            else:  # 晚上 3 节课
                return QColor( 224, 250, 220 )  # 浅绿色
        # 设置文本居中对齐
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        
        return None
    
    def setData( self, index, value, role = Qt.ItemDataRole.EditRole ):
        """
        编辑数据
        :param index:
        :param value:
        :param role:
        :return:
        """
        if role == Qt.ItemDataRole.EditRole:
            item = self.course_data[index.row()][index.column()]
            item.weekday = self.days[index.column()]
            item.period = self.periods[index.row()]
            item.subject = value
            item.modified = True
            self.dataChanged.emit( index, index )
            return True
        return False
    
    def flags( self, index ):
        """
        设置单元格可编辑
        :param index:
        :return:
        """
        return super().flags( index ) | Qt.ItemFlag.ItemIsEditable
    
    def headerData( self, section, orientation, role = Qt.ItemDataRole.DisplayRole ):
        """
        设置表头
        :param section:
        :param orientation:
        :param role:
        :return:
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.days[section]
            if orientation == Qt.Orientation.Vertical:
                return self.periods[section]
        # 设置表头文本居中对齐
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        return None


class CourseEditWnd( QDialog ):
    """课程表窗口"""
    
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.setWindowTitle( "课程表" )
        self.dialogStlManager = SheetManager( dialogStyleSheet )  # 对话框样式表管理器
        self.viewStlManager = SheetManager( ViewStyleSheet )  # 表格视图样式表管理器
        self.headStlManager = SheetManager( HeadStyleSheet )  # 表头样式表管理器
        self.model = CourseTableModel()  # 设置表格模型
        
        self.setStyleSheet( self.dialogStlManager.getStyleSheet() )
        self.initUI()
        self.setWndGeometry()
    
    def initUI( self ):
        """初始化UI"""
        # 创建表格视图
        self.table_view = QTableView( self )
        self.table_view.setStyleSheet( ViewStyleSheet )
        self.table_view.setModel( self.model )
        # 设置选择行为为选择单元格
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems,
        )
        
        # 设置水平和垂直标题栏的样式表
        horizontal_header = self.table_view.horizontalHeader()
        vertical_header = self.table_view.verticalHeader()
        horizontal_header.setStyleSheet( self.headStlManager.getStyleSheet() )
        vertical_header.setStyleSheet( self.headStlManager.getStyleSheet() )
        vertical_header.setDefaultSectionSize( 40 )
        
        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget( self.table_view )
        self.setLayout( layout )
    
    def show( self ):
        """显示窗口"""
        logger.info( "打开课程表窗口" )
        super().show()
    
    def closeEvent( self, event: QCloseEvent ):
        """处理窗口关闭事件，保存数据到数据库"""
        db = self.model.dbMgr
        
        def editRecord( contentItem: ScheduleItem ):
            """修改记录"""
            filterCondition = (
                f"weekday = '{contentItem.weekday}' and period = '{contentItem.period}'"
            )
            db.model.setFilter( filterCondition )
            db.model.select()
            if db.model.rowCount() > 0:
                filteredRecord = db.model.record( 0 )
                filteredRecord.setValue( "course", contentItem.subject )
                db.model.submitAll()
                db.model.setFilter( "" )
                db.model.select()
                logger.info(
                    f"编辑课程表：修改[{contentItem.weekday} {contentItem.period} {contentItem.subject}]",
                )
                return True
            return False
        
        def addRecord( contentItem: ScheduleItem ):
            """添加记录"""
            newRecord = db.model.record()
            newRecord.setValue( "weekday", contentItem.weekday )
            newRecord.setValue( "period", contentItem.period )
            newRecord.setValue( "course", contentItem.subject )
            db.model.insertRecord( -1, newRecord )
            db.model.submitAll()
            db.model.setFilter( "" )
            db.model.select()
            logger.info(
                f"编辑课程表：添加[{contentItem.weekday} {contentItem.period} {contentItem.subject}]",
            )
            return True
        
        def removeRecord( contentItem: ScheduleItem ):
            """删除记录"""
            filterCondition = (
                f"weekday = '{contentItem.weekday}' and period = '{contentItem.period}'"
            )
            db.model.setFilter( filterCondition )
            db.model.select()
            if db.model.rowCount() > 0:
                db.model.removeRow( 0 )
                db.model.submitAll()
                db.model.setFilter( "" )
                db.model.select()
                logger.info(
                    f"编辑课程表：删除[{contentItem.weekday} {contentItem.period} {contentItem.subject}]",
                )
                return True
            return False
        
        for row in range( self.model.rowCount() ):
            for col in range( self.model.columnCount() ):
                item = self.model.course_data[row][col]
                if item.modified and len( item.subject.strip() ) > 0:
                    # 修改数据或添加数据
                    if not editRecord( item ):
                        addRecord( item )
                    item.modified = False
                elif item.modified and len( item.subject.strip() ) == 0:
                    # 删除数据
                    if removeRecord( item ):
                        pass
                    item.modified = False
        
        logger.info( "关闭课程表窗口" )
        event.accept()
    
    def setWndGeometry( self ):
        """设置窗口位置和大小"""
        screen = Screens.primeryScreen
        if screen is None:
            return
        screenGeometry = screen.availableGeometry()
        screenWidth = screenGeometry.width()
        screenHeight = screenGeometry.height()
        self.resize(
            int( screenWidth * 0.6 ),
            int( screenHeight * 0.8 ),
        )
        self.move(
            int( screenWidth * 0.2 ),
            int( screenHeight * 0.1 ),
        )


if __name__ == "__main__":
    app = QApplication( [] )
    Screens.getScreenInfo( app )
    window = CourseEditWnd()
    
    window.show()
    app.exec()
