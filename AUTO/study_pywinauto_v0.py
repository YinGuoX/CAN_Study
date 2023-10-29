# 官方文档代码
import time

from pywinauto.application import Application
from pywinauto.findwindows import find_elements
from  pywinauto.backend import registry
# 1. 启动、连接客户端
# 启动客户端
# app = Application(backend="uia").start("notepad.exe")
# 连接客户端
app = Application(backend="uia").connect(title_re="微信")
print(app.windows())

# 查看Windows系统下所有的窗口
eles = find_elements(backend='uia')
print(eles)

# 2.元素架构
# 获取对话框
dlg = app.window(title_re='微信')
# 打印对话框里面的元素
# dlg.print_control_identifiers()

# 3. backend参数意义？
#       uia：    MS UI　Automation:   WinForms、WPF、Store apps、QT5、浏览器
#       win32：  Win32 API:           MFC、VB6、VCL、简单的WinForms控件和大多数旧的遗留应用程序

# 4. 元素定位
# 4.1 定位工具：
#       https://github.com/blackrosezy/gui-inspect-tool
#       https://github.com/pywinauto/py_inspect
# 4.2 定位方式
#       1. window获取 ： 客户端的对话框
#       2. [属性] ： 根据属性选择元素：dlg['Edit1'].set_text("xxx")
#       3. dlg.属性：根据属性选择元素：dlg.Edit1.set_text("xxx")
#       4. child_window：子窗口定位：dlg.child_window(best_match='登录Button').click_input()

# 定位对话框的 设置 元素，并且绘制一个红框
# dlg['设置'].draw_outline(colour='red')
# 不推荐使用
# dlg.关闭.draw_outline(colour='red')
# 推荐使用:子窗口定位：本质上还是使用find_element()方法
# ele = dlg.child_window(best_match="登录")
# ele.draw_outline(colour='red')

# 4.3 定位属性
#       查阅 find_elements()的源码;主要使用title、best_match等
#       best_match：最佳匹配，返回最佳匹配的第一个元素
dlg.print_control_identifiers()
'''
Pane - '微信'    (L857, T508, R1277, B1078)
['微信', '微信Pane', 'Pane', 'Pane0', 'Pane1', '微信0', '微信1'] =>best_match可以使用的;eg:find_elements(best_match="微信0")
child_window(title="微信", control_type="Pane") =>可以直接用来定位的,当元素复杂时可能会有问题;因为会定位到多个元素
   | 
   | Pane - ''    (L838, T489, R1296, B1097)
   | ['KingPane', 'Pane2', 'KingPane0', 'KingPane1']
   | 
   | Pane - ''    (L857, T508, R1277, B1078)
   | ['KingPane2', 'Pane3']
   |    | 
   |    | Pane - ''    (L857, T508, R1277, B1078)
   |    | ['KingPane3', 'Pane4']
   |    |    | 
   |    |    | Pane - ''    (L857, T508, R1277, B553)
   |    |    | ['Pane5']
   |    |    |    | 
   |    |    |    | Button - '微信'    (L872, T517, R1175, B547)
   |    |    |    | ['微信2', 'Button', '微信Button', 'Button0', 'Button1']
   |    |    |    | child_window(title="微信", control_type="Button")
'''
ele = dlg.child_window(title="微信", control_type="Button")
ele.draw_outline(colour='red')

# 当有多个元素相同时，还是需要使用 find_elements()去定位
# parent参数用于指定查找元素的父级容器
eles = find_elements(control_type="Button",parent=dlg.element_info,top_level_only=False)
print(eles)
for ele in eles:
    # AttributeError: 'UIAElementInfo' object has no attribute 'draw_outline'=>需要包装类型
    ele = registry.backends['uia'].generic_wrapper_class(ele)
    print(ele.texts())
    ele.draw_outline(colour='red')



'''
5. 元素的属性:但是怎么知道 元素是否有这些属性：使用代码
    输入使用：set_text()
    点击使用：click()、click_input()
    获取使用：texts()

ele = dlg.child_window(best_match='xx')
print(dir(ele.element_info))
'''
ele = dlg.child_window(best_match='登录',control_type="Button")
print(dir(ele.element_info))

'''
6. 显式等待与隐式等待
    1. 隐式等待：自带，可以前后设置10倍
    Timings.Fast()
    2. 显式等待：自己实现，根据元素属性，实现
    
'''
#
# def wait_until_enabled(kwargs,wait_time=10,interval_time=0.5):
#     """
#     显式等待；等待元素状态是可用的
#     :param kwargs: 元素定位参数
#     :param wait_time:等待多久
#     :param interval_time:隔多久去检验一次
#     :return:
#     """
#     my_wait_time=0
#     while my_wait_time<wait_time:
#         time.sleep(interval_time)
#         ele = dlg.child_window(**kwargs)
#         print(dir(ele.element_info))
#         print(ele.element_info.enabled)
#         if ele.element_info.enabled:
#             break
#
# wait_until_enabled({"best_match":'登录',"control_type":"Button"})

'''
7. 相对定位:先获取父元素，再获取子元素
    获取父元素：father = dlg.child_window(best_math="xxx")
    打印父元素下面的子元素的信息：father.print_control_identifiers()
    获取子元素：father.child_window(best_math="xxx")
    
8. 菜单选择:分清楚：menu、menu_item
    级联菜单选择：Menu
        dlg.menu_select("File -> Export Session")
        类型必须为：
            control_type = "Menu"
    子菜单的选择：Menu_Item
        子菜单选择：ele.select()
        子菜单类型：control_type = "MenuItem"

eg:
# 点击级联菜单
dlg.menu_select("File -> Export Session")
# 点击级联菜单后，点击里面的子菜单项
menu_item = dlg.child_window(best_match = "All Sessions ...")
menu_item.select()


9. Combox(弹框)选项的选择
    1. 法一：点出下拉框后再点击选项
        dlg.child_window(best_match='ComboxBox').click_input()
        dlg.child_window(best_match='菜单名').click_input()
    2. 法二：dlg.child_window(best_match='ComboxBox').select('菜单名')
    
10. 文件对话框操作
    pywinauto可以直接定位文件对话框！所以直接定位即可
    dlg.child_window(title='文件名:'，control_type='Edit').set_text('测试路径')
'''