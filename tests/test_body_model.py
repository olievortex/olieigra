"""Unit tests for module body_model"""
import unittest
from src import olieigra


class BodyModelTests(unittest.TestCase):
    """Unit tests for class BodyModel"""

    def test_init_initializes_success(self):
        """See if we can create an instance"""
        # arrange, act
        model = olieigra.BodyModel("a", 1, 2, 3, 4, 5, 6, 7)

        # act
        self.assertIsInstance(model, olieigra.BodyModel)
        self.assertEqual("a", model.type)
        self.assertEqual(1, model.pres)
        self.assertEqual(2, model.gph)
        self.assertEqual(3, model.temp)
        self.assertEqual(4, model.rh)
        self.assertEqual(5, model.dpdp)
        self.assertEqual(6, model.wdir)
        self.assertEqual(7, model.wspd)
