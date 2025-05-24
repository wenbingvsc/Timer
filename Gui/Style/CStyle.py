"""PySide样式表管理工具类"""

import re


class SheetManager:
    """PySide样式表管理工具类"""
    
    def __init__( self, styleSheet: str = "" ):
        self.styles = { }  # 样式表
        self.sheetName = ""  # 规则名称
        if styleSheet:
            self.splitSheet( styleSheet )
    
    def setStyle( self, name, style ):
        """设置样式"""
        self.styles[ name ] = style
    
    def addStyle( self, name, style ):
        """添加样式"""
        self.styles[ name ] = style
    
    def getStyle( self, name ) -> str:
        """获取样式"""
        return self.styles.get( name, None )
    
    def removeStyle( self, name ):
        """移除样式"""
        if name in self.styles:
            del self.styles[ name ]
    
    def getFontSize( self ) -> int:
        """获取字体大小"""
        if "font-size" not in self.styles:
            return 0
        sizeString = self.styles[ "font-size" ]
        if sizeString.endswith( "px" ):
            return int( sizeString[ :-2 ] )
        else:
            return int( sizeString )
    
    def splitSheet( self, sheet: str ):
        """
        拆分样式表,初始化实例对象
        样式表格式：
        类型一：
        ‘QLabel{
                font-family: 黑体;
                font-size: 20px;
                font-weight: 400;
                color: #abb2bf;
                background: rgba(255, 255, 255, 0);
                border: 1px solid rgba(255, 255, 255, 0.03);
            }’
        类型二：
        ‘       font-family: 黑体;
                font-size: 20px;
                font-weight: 400;
                color: #abb2bf;
                background: rgba(255, 255, 255, 0);
                border: 1px solid rgba(255, 255, 255, 0.03);
        ’

        类型三：
        ‘
        QHeaderView::section {
                font-family: Arial;
                font-size: 16px;
                font-weight: 400;
                color: #000000;
                border: 1px solid #cccccc;
                background-color: #f0f0f0;
            }
        ’
        """
        # 使用正则表达式匹配样式规则
        pattern = r"([\w+:]+)\s*\{([^{}]*)\}"  # 多个捕获组（多个括号）,返回一个元组列表，每个元组包含每个匹配中所有捕获组的内容。
        matches = re.findall( pattern, sheet, re.DOTALL )
        # 提取规则名称和规则内容
        if matches:
            self.sheetName = matches[ 0 ][ 0 ].strip( )
            rule_content = matches[ 0 ][ 1 ].strip( )
        else:
            rule_content = sheet.strip( )
            self.sheetName = "unknown"
        self.styles = self.splitStyles( rule_content )
    
    @staticmethod
    def splitStyles( rule: str ) -> dict:
        """拆分样式规则"""
        # 使用正则表达式匹配样式规则
        pattern = r"([0-9a-zA-Z-]+)\s*:\s*([^;]+);"
        matches = re.findall( pattern, rule )
        # 提取规则名称和规则内容
        rules = { }  # 定义字典，用于存储规则名称和规则内容
        for match in matches:
            rule_name = match[ 0 ].strip( )
            rule_content = match[ 1 ].strip( )
            rules[ rule_name ] = rule_content
        return rules
    
    def getStyleSheet( self ) -> str:
        """合并样式表"""
        merged_sheet = f"{self.sheetName} {{\n"
        for rule_name, rule_content in self.styles.items( ):
            merged_sheet += f"    {rule_name}: {rule_content};\n"
        merged_sheet += "}"
        return merged_sheet
