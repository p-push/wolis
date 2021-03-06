from wolis.test_case import WolisTestCase
from wolis import utils
import lxml.etree
import webracer.utils

xpath_first_check = webracer.utils.xpath_first_check

class SearchPaginationTest(WolisTestCase):
    def test_one_result_page(self):
        url = '/search.php?keywords=welcome'
        self.get(url)
        self.assert_successish()
        
        assert 'Search found 1 match' in self.response.body
        # remove highlighting
        response_text = utils.naive_strip_html(self.response.body)
        assert 'Welcome to phpBB' in response_text
        
        # it is in a title attribute
        assert 'Click to jump to page' not in self.response.body
    
    def test_many_result_pages(self):
        url = '/search.php?keywords=fancy'
        self.get(url)
        self.assert_successish()
        
        assert 'Search found' in self.response.body
        # remove highlighting
        response_text = utils.naive_strip_html(self.response.body)
        assert 'Fancy post' in response_text
        
        assert 'Click to jump to page' in self.response.body
        
        # check active page
        current_page = self.find_current_page()
        assert current_page == 1
    
    def test_legitimate_offset(self):
        url = '/search.php?keywords=fancy&start=10'
        self.get(url)
        self.assert_successish()
        
        assert 'Search found' in self.response.body
        # remove highlighting
        response_text = utils.naive_strip_html(self.response.body)
        assert 'Fancy post' in response_text
        
        assert 'Click to jump to page' in self.response.body
        
        # check active page
        current_page = self.find_current_page()
        assert current_page == 2
    
    def test_negative_offset(self):
        url = '/search.php?keywords=fancy&start=-10'
        self.get(url)
        self.assert_successish()
        
        assert 'Search found' in self.response.body
        # remove highlighting
        response_text = utils.naive_strip_html(self.response.body)
        assert 'Fancy post' in response_text
        
        assert 'Click to jump to page' in self.response.body
        
        # check active page
        current_page = self.find_current_page()
        assert current_page == 1
    
    @utils.restrict_phpbb_version('>=3.1.0')
    def test_excessive_positive_offset(self):
        url = '/search.php?keywords=fancy&start=1000'
        self.get(url)
        self.assert_successish()
        
        assert 'Search found' in self.response.body
        # remove highlighting
        response_text = utils.naive_strip_html(self.response.body)
        assert 'Fancy post' in response_text
        
        assert 'Click to jump to page' in self.response.body
        
        # check active page
        current_page = self.find_current_page()
        assert current_page == 3

if __name__ == '__main__':
    import unittest
    unittest.main()
