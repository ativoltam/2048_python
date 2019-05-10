import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from app import app


import unittest

class FlaskTestCase(unittest.TestCase):
	# Ensure that flask application was set up correctly
	def test_index(self):
		tester = app.test_client(self)
		response = tester.get('/')
		self.assertEqual(response.status_code, 200)

	def test_games(self):
		tester = app.test_client(self)
		response = tester.get('/api/games')
		self.assertEqual(response.status_code, 200)

	def test_new_game(self):
		tester = app.test_client(self)
		response = tester.get('/api/new_game')
		self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
		unittest.main()