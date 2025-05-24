from PySide6.QtCore import QDate, QPoint, QSize, Qt, Slot
from PySide6.QtWidgets import QColorDialog, QGridLayout, QPushButton

from Gui.Style import SheetManager
from Gui.Widget import CLabel, CWnd
from Utils import Config, logger


class CalendarWidget( CWnd ):
    """日历控件"""
    
    def __init__( self, parent = None ):
        super().__init__( parent = parent )
        self.posMoved.connect( self.onPosMoved )
        self.__currentDate = QDate.currentDate()
        self.setFixedSize( QSize( 140, 160 ) )
        self.setContentsMargins( 0, 0, 0, 0 )
        
        self.__labelSize = QSize(
            int( self.width() * 0.96 / 7 ),
            int( self.height() * 0.96 / 8 ),
        )
        
        self.__initUI()
        
        self.funcSetColor = self.actionOnSetColor
    
    def __initUI( self ):
        """创建日历界面"""
        
        # 创建布局
        main_layout = QGridLayout( self )  # 布局设置父控件时不需要parent参数
        main_layout.setContentsMargins( 0, 0, 0, 0 )  # 设置布局的边距
        main_layout.setSpacing( 3 )  # 设置布局的间距
        main_layout.setAlignment( Qt.AlignmentFlag.AlignCenter )  # 居中对齐
        
        # 创建上一月和下一月按钮
        self.prev_button = QPushButton( "<<", parent = self )
        self.prev_button.setFixedSize( self.__labelSize )
        self.prev_button.clicked.connect( self.prevMonth )
        
        self.next_button = QPushButton( ">>", parent = self )
        self.next_button.setFixedSize( self.__labelSize )
        self.next_button.clicked.connect( self.nextMonth )
        
        # 创建显示当前年月的标签
        self.month_label = CLabel( parent = self )
        self.month_label.sampleStr = "2024aa10aa"
        self.month_label.setContentsMargins( 1, 1, 1, 1 )
        self.month_label.setFixedSize(
            self.__labelSize.width() * 5,
            self.__labelSize.height(),
        )
        
        self.__updateMonthLabel()
        
        # 将按钮和标签添加到布局
        rowIndex = 0
        colIndex = 0
        main_layout.addWidget(
            self.prev_button,
            rowIndex,
            colIndex,
            1,
            1,
            Qt.AlignmentFlag.AlignCenter,
        )
        colIndex += 1
        main_layout.addWidget(
            self.month_label,
            rowIndex,
            colIndex,
            1,
            5,
            Qt.AlignmentFlag.AlignCenter,
        )
        colIndex += 5
        main_layout.addWidget(
            self.next_button,
            rowIndex,
            colIndex,
            1,
            1,
            Qt.AlignmentFlag.AlignCenter,
        )
        
        # 创建星期几的标签
        self.wkdLabels = []
        week_days = ["一", "二", "三", "四", "五", "六", "日"]
        rowIndex = 1
        colIndex = 0
        for day in week_days:
            label = CLabel( parent = self )
            label.setContentsMargins( 1, 1, 1, 1 )
            label.setFixedSize( self.__labelSize )
            label.setText( day )
            main_layout.addWidget(
                label,
                rowIndex,
                colIndex,
                1,
                1,
                Qt.AlignmentFlag.AlignCenter,
            )
            colIndex += 1
            self.wkdLabels.append( label )
        
        # 创建显示日期的网格布局
        self.dateLabels = []
        rowIndex += 1
        colIndex = 0
        # 创建日期标签
        for i in range( 6 ):
            row = []
            for j in range( 7 ):
                label = CLabel( parent = self )
                label.setContentsMargins( 1, 1, 1, 1 )
                label.setFixedSize( self.__labelSize )
                main_layout.addWidget(
                    label,
                    rowIndex,
                    colIndex + j,
                    1,
                    1,
                    Qt.AlignmentFlag.AlignCenter,
                )
                row.append( label )
            rowIndex += 1
            self.dateLabels.append( row )
        
        # 更新日历显示
        self.updateCalendar()
    
    def __updateMonthLabel( self ):
        """更新显示当前年月的标签"""
        self.month_label.setText( self.__currentDate.toString( "yyyy年MM月" ) )
    
    def updateCalendar( self ):
        """更新日历显示"""
        # Get today's date
        today = QDate.currentDate()
        
        # 获取当前月份的第一天
        first_day = QDate( self.__currentDate.year(), self.__currentDate.month(), 1 )
        # 获取当前月份的天数
        days_in_month = first_day.daysInMonth()
        # 获取第一天是星期几
        day_of_week = first_day.dayOfWeek()
        
        # 清空日历
        for row in self.dateLabels:
            for label in row:
                label.setText( "" )
        
        # 填充日期
        day = 1
        for i in range( 6 ):
            for j in range( 7 ):
                if (i == 0 and j < day_of_week - 1) or day > days_in_month:
                    continue
                label = self.dateLabels[i][j]
                label.setText( str( day ) )
                # Highlight today's date
                if (
                        self.__currentDate.year() == today.year()
                        and self.__currentDate.month() == today.month()
                        and day == today.day()
                ):
                    self.setTransparent( label, 0.2 )
                else:
                    self.setTransparent( label, 0.01 )
                day += 1
        
        # 更新月份标签
        self.__updateMonthLabel()
        logger.info( f"更新日历显示：{self.__currentDate.toString( 'yyyy年MM月' )}" )
    
    @staticmethod
    def setTransparent( tLabel: CLabel, alpha: float ):  # 这里将参数类型改为 float
        """设置标签的背景透明度"""
        styleMgr = tLabel.styleManager
        styleMgr.setStyle( "background-color", f"rgba(255, 255, 255, {alpha})" )
        tLabel.setStyleSheet( styleMgr.getStyleSheet() )
    
    def prevMonth( self ):
        """切换到上一个月"""
        self.__currentDate = self.__currentDate.addMonths( -1 )
        self.updateCalendar()
    
    def nextMonth( self ):
        """切换到下一个月"""
        self.__currentDate = self.__currentDate.addMonths( 1 )
        self.updateCalendar()
    
    def actionOnSetColor( self ):
        """设置颜色"""
        """颜色设置函数,Callback函数"""
        color = QColorDialog.getColor(
            parent = self, options = QColorDialog.ColorDialogOption.ShowAlphaChannel,
        )
        if color.isValid():
            # 将选择的颜色转换为十六进制字符串
            color_str = color.name()
            Config.setValue( "colors", "calendartextcolor", color_str )
            self.setColor( color_str )
    
    def setColor( self, color: str ):
        """设置颜色"""
        for row in self.dateLabels:
            for label in row:
                label.setTextColor( color )
        for label in self.wkdLabels:
            label.setTextColor( color )
        self.month_label.setTextColor( color )
        stylemgr = SheetManager()  # 创建样式管理器
        stylemgr.splitSheet( self.prev_button.styleSheet() )  # 拆分样式表,获取现有样式表
        stylemgr.sheetName = "QPushButton"  # 设置样式表名称（避免现有样式表为空）
        stylemgr.setStyle( "color", color )
        self.prev_button.setStyleSheet( stylemgr.getStyleSheet() )
        self.next_button.setStyleSheet( stylemgr.getStyleSheet() )
    
    @Slot( QPoint )
    def onPosMoved( self, pos ):
        """
        处理窗口位置移动事件
        :param pos: 窗口新的位置
        """
        Config.setValue( "wndposition", "CalendarWidgetPos", f"{pos.x()},{pos.y()}" )
