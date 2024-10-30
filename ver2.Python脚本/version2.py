#!/usr/bin/env python
# -*- encoding=utf8 -*-

"""
Description: 同济大学校园网自动登录 version2，增加了切换到 TJ-DORM-WIFI 的功能
Author: Hyoung Yan
Created time: 2024-10-29
Last Modified time: 2024-10-29
"""
import asyncio
from win11toast import toast
import requests
import os
import time

# ---------相关参数-----------
LOGIN_IP = "http://172.21.0.54/"
NOT_SIGNED_IN_TITLE = "上网登录页"
RESULT_RETURN = '"result":1'
TIMEOUT = 1  # 超时时间设置
RETRY_DELAY = 3  # 重试延迟时间（秒）
MAX_RETRIES = 4  # 最大重试次数

# 登录参数 (可以通过环境变量或配置文件获取)
USERNAME = "你的学号"
PASSWORD = "你的密码"
SIGN_PARAMETER = f"http://172.21.0.54/drcom/login?callback=dr1003&DDDDD={USERNAME}&upass={PASSWORD}&0MKKey=123456&R1=0&R2=&R3=0&R6=0&para=00&v6ip=&terminal_type=1&lang=zh-cn&jsVersion=4.1&v=2952&lang=zh"
# 登录成功后的页面标题
SIGNED_IN_TITLES = ["登录成功页", "注销页"]

# 图标路径 (可以使用网络图标或本地文件)
ICONS_PATH = "D:/MyCode/Python/Misc/Tongji-DORM-WiFi-Auto-Login/icons/"
ALREADY_ICON = os.path.join(ICONS_PATH, "Tips.ico")
SUCCESS_ICON = os.path.join(ICONS_PATH, "Check.ico")
FALSE_ICON = os.path.join(ICONS_PATH, "Cross.ico")
UNKNOWN_ICON = os.path.join(ICONS_PATH, "Questionmark.ico")


# ---------辅助函数-----------
async def show_notification(title, msg, icon=None, duration=5):
    """异步显示Windows通知"""
    duration_str = str(duration)
    await toast(
        title,
        msg,
        icon=icon,
        duration=duration_str,
        on_click="https://github.com/yzlevol",
    )


def check_login_status(req_text):
    """检查是否已经登录"""
    return any(title in req_text for title in SIGNED_IN_TITLES)


def switch_to_dorm_wifi():
    """切换到 TJ-DORM-WIFI"""
    # switch_wifi_cmd = 'netsh wlan connect name="TJ-DORM-WIFI"'
    switch_wifi_cmd = r'C:\\Windows\\System32\\netsh wlan connect name="TJ-DORM-WIFI"'
    print("正在切换到 TJ-DORM-WIFI...")
    res = os.system(switch_wifi_cmd)
    if res == 0:
        print("WiFi 切换成功，等待 5 秒...")
        time.sleep(5)  # 等待 WiFi 连接完成
    else:
        print("WiFi 切换失败，重试中...")
        return False
    return True


def is_connected():
    """检查是否连接到校园网"""
    try:
        response = requests.get(LOGIN_IP, timeout=TIMEOUT)
        return True if response.status_code == 200 else False
    except requests.exceptions.RequestException:
        return False


# ---------主程序-----------
# 切换到 TJ-DORM-WIFI
if not switch_to_dorm_wifi():
    asyncio.run(show_notification("切换到TJ-DORM-WiFi失败", "校园网状态", UNKNOWN_ICON))
    os._exit(1)

# 重试连接并执行登录操作
retry_count = 0
while retry_count < MAX_RETRIES:
    # 判断是否已经连接到校园网
    if is_connected():
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
                    asyncio.run(
                        show_notification("登录成功", "校园网状态", SUCCESS_ICON)
                    )
                    os._exit(0)
                else:
                    asyncio.run(show_notification("登录失败", "校园网状态", FALSE_ICON))
            except requests.exceptions.RequestException:
                asyncio.run(show_notification("登录请求失败", "校园网状态", FALSE_ICON))
            os._exit(0)
    else:
        retry_count += 1
        print("未自动连接到校园网，等待重试...重试次数：", retry_count)
        time.sleep(RETRY_DELAY)

# 如果达到最大重试次数仍未成功
asyncio.run(show_notification("未能连接到校园网", "校园网状态", UNKNOWN_ICON))
os._exit(1)
