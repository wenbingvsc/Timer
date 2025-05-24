"""创建QTableView窗口，用于数据库数据的显示和编辑"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import (
    QDialog,
    QMenu,
    QStyledItemDelegate,
    QTableView,
    QTabWidget,
    QVBoxLayout,
)

from Gui.Style import SheetManager
from Model import closeDb, connectToDb, createDbTable
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


class CenteredItemDelegate( QStyledItemDelegate ):
    """自定义委托类，用于居中显示单元格内容"""
    
    def initStyleOption( self, option, index ):
        """初始化样式选项"""
        super().initStyleOption( option, index )
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter


class TableView( QTableView ):
    """自定义QTableView类，用于显示和编辑数据"""
    
    def __init__( self, parent = None, model = None ):
        super().__init__( parent )
        self.setModel( model )
        self.viewStyleManager = SheetManager( ViewStyleSheet )
        self.headStlManager = SheetManager( HeadStyleSheet )
        self.setStyleSheet( self.viewStyleManager.getStyleSheet() )
        
        # 设置水平和垂直标题栏的样式表
        horizontal_header = self.horizontalHeader()
        vertical_header = self.verticalHeader()
        
        horizontal_header.setStyleSheet( self.headStlManager.getStyleSheet() )
        vertical_header.setStyleSheet( self.headStlManager.getStyleSheet() )
        vertical_header.setDefaultSectionSize( 40 )
        
        # 设置自定义委托, 用于居中显示单元格内容
        delegate = CenteredItemDelegate()
        self.setItemDelegate( delegate )
    
    def contextMenuEvent( self, event ):
        """处理鼠标右键点击事件，显示上下文菜单"""
        menu = QMenu( self )
        
        insert_action = QAction( "插入记录", self )
        insert_action.triggered.connect( self.insert_row_before )
        menu.addAction( insert_action )
        
        add_action = QAction( "添加记录", self )
        add_action.triggered.connect( self.add_record )
        menu.addAction( add_action )
        
        delete_action = QAction( "删除记录", self )
        delete_action.triggered.connect( self.delete_record )
        menu.addAction( delete_action )
        
        menu.exec( event.globalPos() )
    
    def add_record( self ):
        """添加新记录到模型"""
        model = self.model()
        if model:
            row = model.rowCount()
            model.insertRow( row )
    
    def insert_row_before( self ):
        """在当前选中行前插入新行"""
        index = self.currentIndex()
        model = self.model()
        if model and index.isValid():
            model.insertRow( index.row() )
    
    def delete_record( self ):
        """删除选中的记录"""
        index = self.currentIndex()
        if index.isValid():
            model = self.model()
            model.removeRow( index.row() )
            model.submitAll()
            model.select()


class ConfigDialog( QDialog ):
    """配置窗口"""
    
    def __init__( self, parent = None, logger = None ):
        super().__init__( parent )
        
        self.setWindowTitle( "配置" )
        self.styleManager = SheetManager( dialogStyleSheet )
        self.setStyleSheet( self.styleManager.getStyleSheet() )
        
        self.db = connectToDb()
        if self.db is not None:
            
            if not createDbTable(
                    self.db,
                    "DailySchedule",
                    ["start_time TEXT", "end_time TEXT", "period TEXT"],
            ):
                logger.error( "创建DailySchedule表失败" )
            
            if not createDbTable(
                    self.db,
                    "CourseSchedule",
                    ["weekday TEXT", "period TEXT", "course TEXT"],
            ):
                logger.error( "创建CourseSchedule表失败" )
            
            if not createDbTable(
                    self.db,
                    "params",
                    ["key TEXT", "value TEXT"],
            ):
                logger.error( "创建params表失败" )
            
            if not createDbTable(
                    self.db,
                    "Countdown",
                    ["dateAndtime TEXT", "description TEXT"],
            ):
                logger.error( "创建Countdown表失败" )
            
            self.dailyScheduleModel = QSqlTableModel( self, self.db )
            self.dailyScheduleModel.setTable( "DailySchedule" )
            self.dailyScheduleModel.select()
            
            self.courseScheduleModel = QSqlTableModel( self, self.db )
            self.courseScheduleModel.setTable( "CourseSchedule" )
            self.courseScheduleModel.select()
            
            self.paramsModel = QSqlTableModel( self, self.db )
            self.paramsModel.setTable( "params" )
            self.paramsModel.select()
            
            self.countdownModel = QSqlTableModel( self, self.db )
            self.countdownModel.setTable( "Countdown" )
            self.countdownModel.select()
        
        else:
            self.db = None
            self.dailyScheduleModel = None
            self.courseScheduleModel = None
            self.paramsModel = None
            self.countdownModel = None
        
        self.createUI()
        self.setWndGeometry()
    
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
    
    def createUI( self ):
        """创建UI界面"""
        self.tab_widget = QTabWidget( self )
        
        self.tab_widget.addTab(
            TableView( self, model = self.dailyScheduleModel ),
            "作息时间",
        )
        self.tab_widget.addTab(
            TableView( self, model = self.courseScheduleModel ),
            "课程表",
        )
        self.tab_widget.addTab(
            TableView( self, model = self.countdownModel ),
            "倒计时",
        )
        self.tab_widget.addTab(
            TableView( self, model = self.paramsModel ),
            "参数",
        )
        
        layout = QVBoxLayout( self )
        layout.addWidget( self.tab_widget )
        layout.setContentsMargins( 0, 0, 0, 0 )
        self.setLayout( layout )
    
    def closeEvent( self, event: QCloseEvent ):
        """处理窗口关闭事件，保存数据到数据库"""
        if hasattr( self, "dailyScheduleModel" ):
            if (
                    self.dailyScheduleModel is not None
                    and not self.dailyScheduleModel.submitAll()
            ):
                logger.error(
                    f"保存作息时间数据失败: {self.dailyScheduleModel.lastError().text()}",
                )
        
        if hasattr( self, "courseScheduleModel" ):
            if (
                    self.courseScheduleModel is not None
                    and not self.courseScheduleModel.submitAll()
            ):
                logger.error(
                    f"保存课程表数据失败: {self.courseScheduleModel.lastError().text()}",
                )
        
        if hasattr( self, "paramsModel" ):
            if self.paramsModel is not None and not self.paramsModel.submitAll():
                logger.error( f"保存参数数据失败: {self.paramsModel.lastError().text()}" )
        
        if hasattr( self, "countdownModel" ):
            if self.countdownModel is not None and not self.countdownModel.submitAll():
                logger.error(
                    f"保存倒数日数据失败: {self.countdownModel.lastError().text()}",
                )
        
        closeDb( self.db )
        logger.info( "关闭配置窗口" )
        event.accept()
