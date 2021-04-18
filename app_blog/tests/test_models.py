from django.test import TestCase
from app_blog.models import Blog


class BlogTestCase(TestCase):
    def setUpTestData(cls):
        print('setup test for class')
        pass

    def setUp(self) -> None:
        print('setup test for any test')
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(True)

    def test_one_plus(self):
        print("Method: test_one plus 1.")
        self.assertEqual(1 + 1, 2, msg='mast be 2')
