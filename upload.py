# encoding=utf-8
import yaml

__author__ = 'pokercc'
import math
import os
import subprocess
import sys
import time

import requests
from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoderMonitor


class Configer:

    def __init__(self, file):
        assert file and os.path.exists(file)
        self.config = yaml.load(file)
        _app = self.config.get('app')
        assert _app
        self.app_project_path = _app.get('project_path')
        self.app_main_module = _app.get('main_module')
        self.update_desc_prefix = _app.get('update_desc_prefix')
        assert self.app_project_path and os.path.exists(self.app_project_path) and self.app_main_module
        _pgyer = self.config.get('pgyer')
        assert _pgyer
        self.pgyer_api_key = _pgyer.get('api_key')
        self.pgyer_app_key = _pgyer.get('app_key')
        self.pgyer_u_key = _pgyer.get('u_key')
        assert self.pgyer_api_key and self.pgyer_app_key and self.pgyer_u_key

        _dingding = self.config.get('dingding')
        self.dingding_access_token = _dingding.get('access_token')


class DingDingRobot:
    """钉钉机器人"""

    def __init__(self, access_token: str):
        assert access_token and isinstance(access_token, str)
        self.access_token = access_token

    def send_message(self, content):
        assert content
        data = {"msgtype": "text", "text": {"content": content}}
        res = requests.post('https://oapi.dingtalk.com/robot/send?access_token={token}'.format(token=self.access_token),
                            json=data)
        res.raise_for_status()
        result = res.json()
        print(result)
        assert result.get('errcode') == 0, f'发送失败'
        print(f'发送成功')


class Giter:

    def get_commit_logs(path, since_time_stamp):
        """

        :param path: 操作目录
        :param since_time_stamp: 起始时机戳
        :return:
        """
        # assert isinstance(int, since_time_stamp)
        assert path and os.path.exists(path)
        cwd = os.getcwd()
        os.chdir(path)
        _shell = "git log --since {since_time_stamp} --pretty=%s".format(since_time_stamp=since_time_stamp)
        result = subprocess.check_output(_shell, encoding='utf-8')
        os.chdir(cwd)
        return str(result).strip()


class Pgyer:
    def __init__(self, api_key, app_key, u_key):
        assert api_key and app_key and u_key
        self.api_key = api_key
        self.app_key = app_key
        self.u_key = u_key

    def get_last_update_time(self):
        """获取上一次pgyer更新的时机戳"""
        r = requests.post('https://www.pgyer.com/apiv2/app/view',
                          data={'_api_key': self.api_key, 'appKey': self.app_key})
        r.raise_for_status()
        res = r.json()
        assert res.get('code') == 0, str(res)
        last_update_time = res.get('data').get('buildUpdated')
        time_struct = time.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(time_struct))

    def upload(self, file, update_desc):
        """
        上传apk到蒲公英
        :param file:
        :param update_desc:
        :return:
        """
        if not update_desc:
            update_desc = input('Please input update desc:\n')

        def print_progressbar(cur, total):
            """打印进度条"""
            percent = '{:.2%}'.format(cur / total)
            sys.stdout.write('\r')
            sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
            if cur == total:  sys.stdout.write('\n')
            sys.stdout.flush()

        def upload_callback(monitor):
            print_progressbar(monitor.bytes_read, monitor.len)

        post_data = {
            'uKey': self.u_key,
            '_api_key': self.api_key,
            'updateDescription': update_desc,
            'file': ('app-debug.apk', open(file, 'rb'), 'application/vnd.android.package-archive'),
        }
        data = MultipartEncoderMonitor(MultipartEncoder(post_data), upload_callback)
        headers = {'Content-Type': data.content_type}
        response = requests.post('https://qiniu-storage.pgyer.com/apiv1/app/upload', data=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(result)
        assert result.get('code') == 0, "上传app失败 %>_<%{}"
        print('上传app成功 O(∩_∩)O')


class Gradle:

    def __init__(self, project_path=os.curdir, main_module='app'):
        assert project_path and os.path.exists(project_path)
        self.project_path = project_path
        self.main_module = main_module
        self.main_module_path = os.path.join(project_path, main_module)

    def build(self):
        cwd = os.getcwd()
        os.chdir(self.project_path)
        os.chmod(path=os.path.join(self.project_path, 'gradlew'), module=777)
        command = 'gradlew {module}:clean {module}:assembleDebug'.format(module=self.main_module)
        assert os.system(command) == 0, "build fail"
        os.chdir(cwd)

    def find_apk(self):
        """查找apk文件"""
        p = os.path.join(self.main_module_path, 'build')
        for root, paths, files in os.walk(p):
            for file in files:
                if str(file).endswith(".apk"):
                    return os.path.join(root, file)

        raise FileNotFoundError("在{path}没有找到apk文件".format(path=p))


def upload():
    print('- read config')
    configer = Configer('config.yml')

    print('- start build app')
    gradle = Gradle(configer.app_project_path, configer.app_main_module)
    gradle.build()

    print('- get last update time stamp')
    pgyer = Pgyer(configer.pgyer_api_key, configer.pgyer_app_key, configer.pgyer_u_key)
    last_update_time = pgyer.get_last_update_time()

    print('- get git commit logs')
    update_desc = Giter(configer.app_project_path).get_commit_logs(last_update_time)
    if not update_desc:
        update_desc = input('请输入更新描述:\n')

    print('- upload apk file')
    pgyer.upload(file=gradle.find_apk(), update_desc=update_desc)

    print('- send dingding message')
    DingDingRobot(configer.dingding_access_token).send_message(configer.update_desc_prefix + update_desc.strip())


if __name__ == '__main__':
    upload()
