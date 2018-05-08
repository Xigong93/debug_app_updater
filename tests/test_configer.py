import os
from unittest import TestCase

from ..upload import Configer

PATH = os.path.abspath(os.path.dirname(__file__))
RES_PATH = os.path.join(PATH, 'res')


class TestConfiger(TestCase):
    def test_correct_config(self):
        configer = Configer(os.path.join(RES_PATH, 'config_correct.yml'))
        self.assertEqual(configer.app_main_module, 'app')
        self.assertEqual(configer.pgyer_u_key, '123456')
        self.assertEqual(configer.dingding_access_token,'abcd')

    def test_error_config_1(self):
        with self.assertRaises(AssertionError):
            configer = Configer(os.path.join(RES_PATH, 'config_error.yml'))
