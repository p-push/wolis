import owebunit
import utils
from wolis_test_case import WolisTestCase

class UpdateTestCase(WolisTestCase):
    def setUp(self):
        super(UpdateTestCase, self).setUp()
        
        #self.clear_cache()
    
    def test_update(self):
        self.get('/install/database_update.php')
        self.assert_successish()

if __name__ == '__main__':
    import unittest
    unittest.main()