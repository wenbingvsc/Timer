"""标签控件基类"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel

from Gui.Style import SheetManager

CLabelSize = QSize( 100, 30 )


class CLabel( QLabel ):
    """标签控件基类,支持自动调整字体大小,包含样式管理器"""
    
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.sampleStr = "ab"
        self.setContentsMargins( 1, 1, 1, 1 )  # 增加一些内边距
        self.styleManager: SheetManager = SheetManager(
            """
            QLabel{
                font-family: 黑体;
                font-size: 20px;
                font-weight: 400;
                color: #abb2bf;
                background: rgba(255, 255, 255, 0.01);
                border: 1px solid rgba(255, 255, 255, 0.03);
            }
            """,
        )  # 初始化样式管理器
        
        self.setStyleSheet( self.styleManager.getStyleSheet() )  # 设置样式
        self.setAlignment( Qt.AlignmentFlag.AlignCenter )  # 文本居中对齐
    
    def setTextColor( self, color: str ):
        """设置文本颜色"""
        self.styleManager.setStyle( "color", color )
        self.setStyleSheet( self.styleManager.getStyleSheet() )  # 设置样式
    
    def adjustFontSize( self ):
        """根据标签大小调整字体大小"""
        rect = self.contentsRect()  # 获取标签的内容区域
        fontSize = self.__calcSuitableSize( rect.width(), rect.height() )
        self.styleManager.setStyle( "font-size", f"{fontSize}px" )  # 修改字体大小
        self.setStyleSheet( self.styleManager.getStyleSheet() )  # 设置样式
    
    def __calcSuitableSize( self, maxWidth, maxHeight ):
        """
        根据最大宽度和高度计算显示指定字符串合适的字体大小
        :param maxWidth: 最大宽度
        :param maxHeight: 最大高度
        :return: 合适的字体大小
        """
        # 计算文本的行数,并拆分为列表
        splitCount = self.sampleStr.count( "\n" )
        textlist = self.sampleStr.split( "\n", splitCount )
        
        # 计算文本的宽度和高度
        fontMetrics = self.fontMetrics()
        textWidthList = []
        for text in textlist:
            textWidth = fontMetrics.horizontalAdvance( text )
            textWidthList.append( textWidth )
        
        textWidth = max( textWidthList )
        textHeight = fontMetrics.height() * len( textlist )
        
        # 计算缩放因子
        widthScale = maxWidth / textWidth
        heightScale = maxHeight / textHeight
        scale = min( widthScale, heightScale )
        # 计算合适的字体大小
        fontSize = int( self.styleManager.getFontSize() * scale )
        return fontSize
    
    def resizeEvent( self, event ):
        """重写resizeEvent方法，在窗口大小改变时调整字体大小"""
        super().resizeEvent( event )
        self.adjustFontSize()
