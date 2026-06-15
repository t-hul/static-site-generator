from unittest import TestCase
from src.utils import copy_tree


class TestCopyTree(TestCase):
    def test_copy_tree(self):
        copy_tree("static", "public")
