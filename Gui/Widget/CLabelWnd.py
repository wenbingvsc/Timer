"""标签窗口基类"""

from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import QColorDialog

from Gui.Widget.baseWnd import CWnd
from Gui.Widget.CLabel import CLabel

winSize = QSize( 100, 50 )  # 应用窗口大小


class CLabelWnd( CWnd ):
    """窗口基类, 包含一个CLabel标签和样式管理器，支持拖动和透明背景"""
    
    colorChanged = Signal( str )  # 文本颜色改变信号
    
    def __init__( self, parent = None ):
        super().__init__( parent )
        self.textLabel: CLabel = CLabel( self )
        self.funcSetColor = self.actionOnSetColor  # 文本颜色设置函数，callback函数
    
    def setText( self, text ):
        """设置文本"""
        if hasattr( self, "textLabel" ) is False:
            return
        self.textLabel.setText( text )
    
    def setTextColor( self, color: str ):
        """设置文本颜色"""
        if hasattr( self, "textLabel" ) is False:
            return
        self.textLabel.setTextColor( color )
        self.colorChanged.emit( color )
    
    def setSampleStr( self, sampleStr: str ):
        """设置示例文本"""
        if hasattr( self, "textLabel" ) is False:
            return
        self.textLabel.sampleStr = sampleStr
    
    def resizeEvent( self, event ):
        """重写resizeEvent方法，在窗口大小改变时调整字体大小"""
        super().resizeEvent( event )
        self.textLabel.setFixedSize( self.size() )
    
    def actionOnSetColor( self ):
        """颜色设置函数,Callback函数"""
        color = QColorDialog.getColor(
            parent = self, options = QColorDialog.ColorDialogOption.ShowAlphaChannel,
        )
        if color.isValid():
            # 将选择的颜色转换为十六进制字符串
            color_str = color.name()
            self.setTextColor( color_str )
