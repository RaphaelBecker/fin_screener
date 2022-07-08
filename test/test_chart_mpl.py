import unittest
import utils.talib_functions as talib_funcs


class TestChartMpl(unittest.TestCase):

    def test_overlap_studies(self):
        list_ = list(talib_funcs.overlap_studies_functions.keys())
        print(list_)