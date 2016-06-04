from ricknmorty import *
import unittest

class ResponseTest(unittest.TestCase):
	def test_response(self):
		self.assertEqual("You pass butter.", decide_on_response('yo what is my purpose'))
		self.assertIn(decide_on_response('you are near me'), PERSONAL_SPACE)

if __name__ == '__main__':
    unittest.main()
