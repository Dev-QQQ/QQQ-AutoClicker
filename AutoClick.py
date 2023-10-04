import ctypes
import time
import threading
import keyboard

# 定义一些Windows API函数和常量
user32 = ctypes.windll.user32

# 定义鼠标点击的常量
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

# 自定义POINT结构
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# 全局变量，用于标记是否启动自动点击和程序是否运行
auto_click_enabled = False
program_running = True

# 模拟鼠标左键单击
def click_mouse():
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 读取鼠标位置
def get_mouse_position():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

# 启动自动点击
def start_auto_click():
    global auto_click_enabled
    auto_click_enabled = True
    while auto_click_enabled:
        x, y = get_mouse_position()
        print(f"当前鼠标位置：x={x}, y={y}")
        
        # 在当前鼠标位置触发点击
        click_mouse()
        
        # 如果鼠标位置在屏幕最左侧，停止自动点击和退出程序
        if x == 0:
            stop_auto_click()
            global program_running
            program_running = False
        
        # 暂停5毫秒
        time.sleep(0.001)

# 停止自动点击
def stop_auto_click():
    global auto_click_enabled
    auto_click_enabled = False

# 监听键盘事件的线程
def keyboard_listener():
    global program_running
    while program_running:
        if keyboard.is_pressed('F6'):  # F6键
            start_auto_click()
        if keyboard.is_pressed('F7'):  # F7键
            stop_auto_click()

# 创建键盘事件监听线程
keyboard_thread = threading.Thread(target=keyboard_listener)

# 启动键盘事件监听线程
keyboard_thread.start()

# 主线程等待键盘事件监听线程
keyboard_thread.join()
