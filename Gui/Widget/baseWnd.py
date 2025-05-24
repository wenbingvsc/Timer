"""窗口基类"""

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QWidget

from Gui.Style import SheetManager


class CWnd( QWidget ):
    """窗口基类, 包含样式管理器，支持拖动和透明背景, 支持右键菜单"""
    
    posMoved = Signal( QPoint )  # 窗口移动信号
    
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.setWindowFlags( Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint )
        self.setAttribute( Qt.WidgetAttribute.WA_TranslucentBackground, True )  # 透明背景
        
        self.styleManager: SheetManager = SheetManager(
            """
            QWidget{
                background-color:rgba(255, 255, 255, 0.01);    
                border: 1px solid rgba(255, 255, 255, 0.01); 
                border-radius: 2px;
                font-family: 黑体;
                font-size: 14px;
                font-weight: 400;
                color: #abb2bf;
            }   
            """,
        )
        self.setStyleSheet( self.styleManager.getStyleSheet() )
        
        self.draggable: bool = True  # 标记窗口是否可拖动
        self.dragging: bool = False  # 标记是否正在拖动
        self.offset = None  # 记录鼠标按下时的偏移量
        
        self.funcSetColor: callable = None  # 文本颜色设置函数，callback函数
    
    def setTransBackground( self, trans: bool = True ):
        """设置窗口是否透明背景，默认透明"""
        self.setAttribute( Qt.WidgetAttribute.WA_TranslucentBackground, on = trans )
    
    def setDraggable( self, draggable: bool = True ):
        """设置窗口是否可拖动, 默认可拖动"""
        self.draggable = draggable
    
    def isOnTop( self ) -> bool:
        """判断窗口是否置顶"""
        return self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint
    
    def setOnTopHint( self, onTop: bool = False ):
        """将窗口置顶, 默认为不置顶"""
        current_flags = self.windowFlags()  # 获取当前窗口标志
        if onTop:
            new_flags = current_flags | Qt.WindowType.WindowStaysOnTopHint
        else:
            new_flags = current_flags & ~Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags( new_flags )  # 设置新的窗口标志
    
    def mousePressEvent( self, event ):
        """
        鼠标按下事件，记录鼠标按下时的偏移量
        说明：
        全局坐标：指的是相对于整个屏幕左上角的坐标，
        event.globalPosition().toPoint()是鼠标在屏幕上的全局位置，
        self.pos()是窗口在屏幕上的位置，
        两者相减得到的是鼠标相对于窗口的偏移量
        """
        if self.draggable and event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.globalPosition().toPoint() - self.pos()
        elif event.button() == Qt.MouseButton.RightButton:
            self.contextMenu( event.globalPosition().toPoint() )
        return super().mousePressEvent( event )
    
    def mouseMoveEvent( self, event ):
        """鼠标移动事件，根据偏移量移动窗口"""
        if self.dragging:
            # 计算窗口在屏幕的全局坐标并移动窗口
            self.move( event.globalPosition().toPoint() - self.offset )
        return super().mouseMoveEvent( event )
    
    def mouseReleaseEvent( self, event ):
        """鼠标释放事件，停止拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.posMoved.emit( self.pos() )
        return super().mouseReleaseEvent( event )
    
    def contextMenu( self, pos: QPoint ):
        """创建上下文菜单"""
        menu = QMenu( self )
        # 添加菜单项
        action1 = QAction( "置顶", self, checkable = True )
        action1.setChecked( self.isOnTop() )
        action1.triggered.connect( self.actionOnTopHint )
        menu.addAction( action1 )
        
        if self.funcSetColor is not None:
            action2 = QAction( "文本颜色", self )
            action2.triggered.connect( self.funcSetColor )
            menu.addAction( action2 )
        
        # 显示菜单
        menu.exec( pos )
    
    def actionOnTopHint( self ):
        """右键菜单中的‘置顶’事件相应"""
        sender: QAction = self.sender()
        self.setOnTopHint( sender.isChecked() )
        self.show()
