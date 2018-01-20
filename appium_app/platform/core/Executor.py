__author__ = 'banketree'

import os
import time

# 查找方法
Find_id = "id"
Find_xpath = "xpath"
Find_xpaths = "xpaths"
Find_class = "class"  # 单个
Find_css = "css"
Find_name = "name"

# 事件
Event_click = "click"
Event_swipeDown = "swipeDown"
Event_swipeUp = "swipeUp"
Event_swipeLeft = "swipeLeft"
Event_swipeRight = "swipeRight"
Event_setValue = "setValue"
Event_getValue = "getValue"
Event_message = "message"
Event_press = "press"
Event_keyevent = "keyevent"
Event_sleep = "sleep"
Event_toWebview = "toWebview"
Event_toNative = "toNative"
Event_equal = "equal"
Event_exist = "exist"
Event_back = "back"
Event_adb = "adb"  # android


# 操作元素
class Executor:
    # 事件  哪个元素--》事件--》参数-->导入的数据
    def event(self, element, eventType="click", params=None, yamlParam=None):
        print("event:" + element + "-->" + eventType + "-->" + params + "-->" + yamlParam)
        try:
            if (eventType == Event_sleep):
                if (params == None):
                    time.sleep(1)
                else:
                    time.sleep(params["second"])
                return True
        except Exception as e:
            print(e)
        return False

    # 查找元素--->find-->findtype:id/ids/xpath -->index
    def find(self, findField, findType='xpath', index=0):
        print("find:" + findField + "-->" + findType + "-->" + index)
        return None

    # 截屏
    def shotScreen(self, filePath, filename):
        pass

    # 获取系统日志
    def getLog(self):
        return ""

    pass


if __name__ == '__main__':
    pass
