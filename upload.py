# encoding=utf-8
# @author  pokercc<pokercc@sina.com>
import json
import math
import os
import subprocess
import sys
import time
from functools import reduce

import requests
from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoderMonitor

# 新的上传地址
from dingding_message import send_message

# pgyer ukey
U_KEY = ''
# pgyer apikey
API_KEY = ''
# pgyer appkey
APP_KEY = ''
# 用户的下载密码
INSTALL_PASSWORD = 'everstar'

MESSAGE_TEMP = '''$app_name更新了!
更新描述:
$content
下载链接 $download_url'''


def send_dingding_msg(msg):
    """发送钉钉通知"""
    assert msg
    send_message(MESSAGE_TEMP.replace('$content', msg))


def print_progressbar(cur, total):
    """打印进度条"""
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
    if cur == total:  sys.stdout.write('\n')
    sys.stdout.flush()


def find_apk(path):
    """查找apk文件"""
    assert path and os.path.exists(path)
    for root, paths, files in os.walk(path):
        for file in files:
            if str(file).endswith(".apk"):
                return os.path.join(root, file)

    raise FileNotFoundError(f"在{path}没有找到apk文件")


def get_last_update_time():
    """获取上一次pgyer更新的时机戳"""
    r = requests.post('https://www.pgyer.com/apiv2/app/view', data={'_api_key': API_KEY, 'appKey': APP_KEY})
    r.raise_for_status()
    res = r.json()
    assert res.get('code') == 0, str(res)
    last_update_time = res.get('data').get('buildUpdated')
    time_struct = time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(time_struct))


def get_git_logs(path, since_time_stamp):
    """

    :param path: 操作目录
    :param since_time_stamp: 起始时机戳
    :return:
    """
    # assert isinstance(int, since_time_stamp)
    assert path and os.path.exists(path)
    cwd = os.getcwd()
    os.chdir(path)
    _shell = f"git log --since {since_time_stamp} --pretty=%s"
    result = subprocess.check_output(_shell, encoding='utf-8')
    os.chdir(cwd)
    return str(result).strip()


# 上传apk到蒲公英
def upload(file, update_desc):
    """
    上传apk到蒲公英
    :param file:
    :param update_desc:
    :return:
    """
    if not update_desc:
        update_desc = input('Please input update desc:\n')

    def upload_callback(monitor):
        print_progressbar(monitor.bytes_read, monitor.len)

    post_data = {
        'uKey': U_KEY,
        '_api_key': API_KEY,
        # 'password': INSTALL_PASSWORD,
        # 'installType': '2',
        'updateDescription': update_desc,
        'file': ('app-debug.apk', open(file, 'rb'), 'application/vnd.android.package-archive'),
    }
    data = MultipartEncoderMonitor(MultipartEncoder(post_data), upload_callback)
    headers = {'Content-Type': data.content_type}
    response = requests.post('https://qiniu-storage.pgyer.com/apiv1/app/upload', data=data, headers=headers)
    response.raise_for_status()
    print(response.json())
    assert response.json().get('code') == 0, "上传app失败 %>_<%{}"
    send_dingding_msg(update_desc.strip())
    print('上传app成功 O(∩_∩)O')


def main():
    argv_length = len(sys.argv)
    print('upload to pgyer start ')
    assert os.system(f'cd ../.. &&gradlew app:clean app:assembleDebug ') == 0, "build fail"

    update_desc = get_git_logs('../../', get_last_update_time())
    if not update_desc:
        update_desc = input('请输入更新描述:\n')
    upload(file=find_apk(f'../../app/build'), update_desc=update_desc)


if __name__ == '__main__':
    main()
    # print(get_git_logs('.', '2018-03-20'))
    # send_dingding_msg(read_update_desc())
