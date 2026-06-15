# import os
# from unittest import TestCase
#
# from src.utils import copy_tree
#
#
# class TestCopyTree(TestCase):
#     def test_copy_tree(self):
#         source = "static"
#         target = "public"
#         source_files = os.listdir(source)
#         copy_tree(source, target)
#         target_files = os.listdir(target)
#         self.assertEqual(source_files, target_files)
