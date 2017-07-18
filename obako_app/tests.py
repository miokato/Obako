from django.test import TestCase
import pandas as pd
import unittest
from obako_app.tools.parser import Parser


class ParserTest(unittest.TestCase):

    def setUp(self):
        path = 'data/akitaben.csv'
        dic = pd.read_csv(path, index_col=0)
        self.parser = Parser(dic)

    def test_parse(self):
        sent = 'こんばんは。今日は寒いですね。'
        parsed = self.parser.parse(sent)
        self.assertEqual(type(parsed), list)



