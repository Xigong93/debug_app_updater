import os
from unittest import TestCase

from ..upload import Pgyer

PATH = os.path.abspath(os.path.dirname(__file__))
RES_PATH = os.path.join(PATH, 'res')


class TestPgyer(TestCase):

    def _setUp(self):
        super().setUp()
        self.pgyer = Pgyer(
            os.getenv("pgyer_api_key"),
            os.getenv("pgyer_app_key"),
            os.getenv("pgyer_u_key")
        )

    def _test_get_last_update_time(self):
        time = self.pgyer.get_last_update_time()
        self.assertIsNotNone(time)
        self.assertIsInstance(time, int)

    def _test_upload(self):
        self.pgyer.upload(os.path.join(RES_PATH, 'demo.apk'), '测试更新')
