from unittest import TestCase

from helpers import *
from main import *

class TestMain(TestCase):
  def setUp(self):
    reset()

  def test_login(self):
    global account_id
    # we are not logged in yet
    self.assertEqual(account_id, None)

    # after login, we should have the account id set to 1
    account_id = login(111111, 1111)
    self.assertEqual(account_id, 1)