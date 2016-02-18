import bottle
import unittest
import webtest

from bountysnakeai import main

TestApp = webtest.TestApp
TestCase = unittest.TestCase

class ControllerTestCase(TestCase):

    def setUp(self):
        super(ControllerTestCase, self).setUp()
        # Enable stack traces in 500 responses
        bottle.debug(True)

    def tearDown(self):
        super(ControllerTestCase, self).setUp()
        # Disable stack traces in 500 responses
        bottle.debug(False)
        # Wipe the test db
        main.db.flushdb()
