"""Unit tests for module header_model"""
import unittest
from src import olieigra


class HeaderModelTests(unittest.TestCase):
    """Unit tests for class HeaderModel"""

    def test_init_initializes_success(self):
        """See if we can create an instance"""
        # arrange, act
        model = olieigra.HeaderModel("a", 1, 2, 3, 4, 5, 6, "b", "c", 7, 8)

        # act
        self.assertIsInstance(model, olieigra.HeaderModel)
        self.assertEqual("a", model.id)
        self.assertEqual(1, model.year)
        self.assertEqual(2, model.month)
        self.assertEqual(3, model.day)
        self.assertEqual(4, model.hour)
        self.assertEqual(5, model.reltime)
        self.assertEqual(6, model.numlev)
        self.assertEqual("b", model.p_src)
        self.assertEqual("c", model.np_src)
        self.assertEqual(7, model.lat)
        self.assertEqual(8, model.lon)
