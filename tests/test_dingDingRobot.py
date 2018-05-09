from unittest import TestCase

from ..upload import DingDingRobot


class TestDingDingRobot(TestCase):
    def test_send_message(self):
        DingDingRobot('access_token').send_message('测试消息')
