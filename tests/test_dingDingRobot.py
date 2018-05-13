import os
from unittest import TestCase

from ..upload import DingDingRobot


class TestDingDingRobot(TestCase):
    def _test_send_message(self):
        access_token = os.getenv('ding_access_token')
        access_token and DingDingRobot(access_token).send_message('测试消息')
