from ricknmorty import *
import unittest

class ResponseTest(unittest.TestCase):
	def test_response(self):
		self.assertEqual("You pass butter.", decide_on_response([{'type': 'message', 'text': 'yo what is my purpose', 'channel': 'test_channel'}]))
		self.assertIn(decide_on_response([{'type': 'message', 'text': 'you are near me', 'channel': 'test_channel'}]), PERSONAL_SPACE)

if __name__ == '__main__':
    unittest.main()
