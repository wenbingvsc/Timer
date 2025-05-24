"""数据校验模块"""
import re


def checkWeekdayString( weekdayString: str ) -> bool:
    """检查星期字符串格式是否正确"""
    pattern = r"^(星期一|星期二|星期三|星期四|星期五|星期六|星期日)$"
    return bool( re.match( pattern, weekdayString ) )


def checkDateString( dateString: str ) -> bool:
    """检查日期字符串格式是否正确"""
    pattern = r"^\d{4}-\d{1,2}-\d{1,2}$"
    return bool( re.match( pattern, dateString ) )


def checkTimeString( timeString: str ) -> bool:
    """检查时间字符串格式是否正确"""
    pattern = r"^\d{1,2}:\d{1,2}$"
    return bool( re.match( pattern, timeString ) )


def checkPeriodString( periodString: str ) -> bool:
    """检查时间段字符串格式是否正确"""
    pattern = r"^(上午|下午|晚上)第[一二三四五六七八九十]+节$|^(课间休息|下班|午休|晚饭时间|休息时间|体育锻炼)$"
    return bool( re.match( pattern, periodString ) )


def formatTimeString( timeString ):
    """
    格式化时间字符串，去除空格，补零，并将时间字符串转换为 hh:mm 格式
    :param timeString: 时间字符串
    :return: 格式化后的时间字符串，格式为 hh:mm
    """
    timeString = timeString.strip()
    timeString = timeString.replace( " ", "" )
    timeString = timeString.replace( "：", ":" )
    # 按冒号分割时间字符串
    parts = timeString.split( ":" )
    if len( parts ) == 2:  # 检查是否有足够的部分
        hour, minute = parts
        # 对小时和分钟进行补零操作
        hour = hour.zfill( 2 )
        minute = minute.zfill( 2 )
        return f"{hour}:{minute}"
    return timeString


def formatDateString( dateString: str ):
    """
    格式化日期字符串,去除空格,补零,并将日期字符串转换为 yyyy-MM-dd 格式
    :param dateString: 日期字符串
    :return: 格式化后的日期字符串, 格式为 yyyy-MM-dd
    """
    dateString = dateString.strip()
    dateString = dateString.replace( " ", "" )
    # 按冒号分割时间字符串
    parts = dateString.split( "-" )
    if len( parts ) == 3:  # 检查是否有足够的部分
        year, month, day = parts
        # 对小时和分钟进行补零操作
        year = year.zfill( 4 )
        month = month.zfill( 2 )
        day = day.zfill( 2 )
        return f"{year}-{month}-{day}"
    return dateString
