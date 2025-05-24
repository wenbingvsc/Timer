"""常量类"""


class Weekday:
    """星期常量"""
    
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    CMONDAY = "星期一"
    CTUESDAY = "星期二"
    CWEDNESDAY = "星期三"
    CTHURSDAY = "星期四"
    CFRIDAY = "星期五"
    CSATURDAY = "星期六"
    CSUNDAY = "星期日"
    CWEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


class Month:
    """月份常量"""
    
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"
    MONTHS = [
        "January", "February", "March", "April",
        "May", "June", "July", "August", "September",
        "October", "November", "December",
    ]
    
    CJANUARY = "一月"
    CFEBRUARY = "二月"
    CMARCH = "三月"
    CAPRIL = "四月"
    CMAY = "五月"
    CJUNE = "六月"
    CJULY = "七月"
    CAUGUST = "八月"
    CSEPTEMBER = "九月"
    COCTOBER = "十月"
    CNOVEMBER = "十一月"
    CDECEMBER = "十二月"
    CMONTHS = [
        "一月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "十一月", "十二月",
    ]


class Period:
    """时间段常量"""
    
    MORNING = "Morning"
    AFTERNOON = "Afternoon"
    EVENING = "Evening"
    NIGHT = "Night"
    PERIODS = ["Morning", "Afternoon", "Evening", "Night"]
    
    CMORNING = "早上"
    CAFTERNOON = "下午"
    CEVENING = "晚上"
    CNIGHT = "深夜"
    CPERIODS = ["早上", "下午", "晚上", "深夜"]


class Subject:
    """科目常量"""
    MATH = "Math"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    BIOLOGY = "Biology"
    HISTORY = "History"
    GEOGRAPHY = "Geography"
    ENGLISH = "English"
    CHINESE = "Chinese"
    POLITICAL_SCIENCE = "Political Science"
    ETHICS_AND_LEGALITY = "Ethics and Legality"
    SPORTS = "Sports"
    INFORMATION_TECHNOLOGY = "Information Technology"
    MUSIC = "Music"
    ARTS = "Arts"
    SCIENCE = "Science"
    POLITICAL_AND_SOCIAL = "Political and Social"
    SPORTS_AND_HEALTH = "Sports and Health"
    LABOR_AND_EMPLOYMENT = "Labor and Employment"
    ART = "Art"
    GENERAL_TECHNOLOGY = "General Technology"
    
    SUBJECTS = [
        "Chinese", "Math", "English", "Physics", "Chemistry",
        "Biology", "Political Science", "History", "Geography",
        "Ethics and Legality", "Political and Social",
        "Information Technology", "Science", "Music", "Arts", "Art",
        "Sports", "Sports and Health", "General Technology",
        "Labor and Employment",
    
    ]
    
    CMATH = "数学"
    CPHYSICS = "物理"
    CCHEMISTRY = "化学"
    CBIOLGY = "生物"
    CHISTORY = "历史"
    CGEOGRAPHY = "地理"
    CENGLISH = "英语"
    CCHINESE = "语文"
    CPOLITICAL_SCIENCE = "政治"
    CETHICS_AND_LEGALITY = "道德与法治"
    CSPORTS = "体育"
    CINFORMATION_TECHNOLOGY = "信息技术"
    CMUSIC = "音乐"
    CARTS = "美术"
    CSCIENCE = "科学"
    CPOLITICAL_AND_SOCIAL = "思想政治"
    CSPORTS_AND_HEALTH = "体育与健康"
    CLABOR_AND_EMPLOYMENT = "劳动与就业"
    CART = "艺术"
    CGENERAL_TECHNOLOGY = "通用技术"
    CSUBJECTS = [
        "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "道德与法治", "思想政治", "信息技术", "科学", "音乐", "美术", "艺术", "体育",
        "体育与健康", "通用技术", "劳动与就业",
    ]


class ClassPeriod:
    """课程时间段常量"""
    MN_FIRST = "上午第一节"
    MN_SECOND = "上午第二节"
    MN_THIRD = "上午第三节"
    MN_FOURTH = "上午第四节"
    MN_FIFTH = "上午第五节"
    AN_FIRST = "下午第一节"
    AN_SECOND = "下午第二节"
    AN_THIRD = "下午第三节"
    AN_FOURTH = "下午第四节"
    AN_FIFTH = "下午第五节"
    EN_FIRST = "晚上第一节"
    EN_SECOND = "晚上第二节"
    EN_THIRD = "晚上第三节"
    EN_FOURTH = "晚上第四节"
    
    CLASS_PERIODS = [
        "上午第一节", "上午第二节", "上午第三节", "上午第四节",
        "下午第一节", "下午第二节", "下午第三节", "下午第四节",
        "晚上第一节", "晚上第二节", "晚上第三节",
    ]
