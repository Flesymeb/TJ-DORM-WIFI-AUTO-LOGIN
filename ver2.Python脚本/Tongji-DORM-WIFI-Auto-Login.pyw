#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Description: 同济大学校园网自动登录
Author: Hyoung Yan
Created time: 2024-10-29 22:54:44
Last Modified time: 2024-10-29 23:54:53
"""

import asyncio
from win11toast import toast
import requests
import os

# ---------相关参数-----------
# 无需修改，或自行配置
LOGIN_IP = "http://172.21.0.54/"
NOT_SIGNED_IN_TITLE = "上网登录页"
RESULT_RETURN = '"result":1'
TIMEOUT = 1  # 超时时间设置

# 登录参数 (可以通过环境变量或配置文件获取)
USERNAME = "你的学号"
PASSWORD = "你的密码"
# 无需修改，或自行配置
SIGN_PARAMETER = f"http://172.21.0.54/drcom/login?callback=dr1003&DDDDD={USERNAME}&upass={PASSWORD}&0MKKey=123456&R1=0&R2=&R3=0&R6=0&para=00&v6ip=&terminal_type=1&lang=zh-cn&jsVersion=4.1&v=2952&lang=zh"


# 登录成功后的页面标题
SIGNED_IN_TITLES = ["登录成功页", "注销页"]


# 图标路径 (可以使用网络图标或本地文件)
ICONS_PATH = (
    "D:/MyCode/Python/Misc/Tongji-DORM-WiFi-Auto-Login/icons/"  # 请修改为你的图标路径
)
ALREADY_ICON = os.path.join(ICONS_PATH, "Tips.ico")
SUCCESS_ICON = os.path.join(ICONS_PATH, "Check.ico")
FALSE_ICON = os.path.join(ICONS_PATH, "Cross.ico")
UNKNOWN_ICON = os.path.join(ICONS_PATH, "Questionmark.ico")


# ---------辅助函数-----------
async def show_notification(title, msg, icon=None, duration=5):
    """异步显示Windows通知"""
    # 将duration设置为字符串类型，确保兼容性
    duration_str = str(duration)
    await toast(
        title,
        msg,
        icon=icon,
        duration=duration_str,
        on_click="https://github.com/yzlevol",  # 点击广告
    )


def check_login_status(req_text):
    """检查是否已经登录"""
    return any(title in req_text for title in SIGNED_IN_TITLES)


# ---------主程序-----------
try:
    response = requests.get(LOGIN_IP, timeout=TIMEOUT)
    req_text = response.text
except requests.exceptions.RequestException:
    req_text = "False"

# 判断是否已经登录
if check_login_status(req_text):
    asyncio.run(show_notification("该设备已经登录", "校园网状态", ALREADY_ICON))
    os._exit(0)

# 判断是否未登录
elif NOT_SIGNED_IN_TITLE in req_text:
    try:
        # 尝试登录
        response = requests.get(SIGN_PARAMETER, timeout=TIMEOUT)
        req_text = response.text

        # 判断是否登录成功
        if RESULT_RETURN in req_text:
            asyncio.run(show_notification("登录成功", "校园网状态", SUCCESS_ICON))
        else:
            asyncio.run(show_notification("登录失败", "校园网状态", FALSE_ICON))
    except requests.exceptions.RequestException:
        asyncio.run(show_notification("登录请求失败", "校园网状态", FALSE_ICON))
    os._exit(0)

# 未连接到校园网
else:
    asyncio.run(show_notification("未连接到校园网", "校园网状态", UNKNOWN_ICON))
    os._exit(0)
