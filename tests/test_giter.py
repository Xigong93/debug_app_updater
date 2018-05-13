import os
from unittest import TestCase

from ..upload import Giter


class TestGiter(TestCase):
    def test_get_commit_logs(self):
        logs = Giter().get_commit_logs(os.curdir, '2018-01-10')
        self.assertIsNotNone(logs)
