import owebunit
import owebunit.utils
import urlparse
from wolis.test_case import WolisTestCase

class AcpLoginTestCase(WolisTestCase):
    def test_acp_login(self):
        self.login('morpheus', 'morpheus')
        
        self.get('/')
        self.assert_successish()
        
        doc = self.response.lxml_etree
        acp_link = owebunit.utils.xpath_first_check(doc, '//div[@class="copyright"]//a[text() = "Administration Control Panel"]').attrib['href']
        acp_link = urlparse.urljoin('/', acp_link)
        
        self.get(acp_link)
        self.assert_successish()
        
        assert 'To administer the board you must re-authenticate yourself.' in self.response.body
        
        assert len(self.response.forms) == 2
        form = self.response.forms[1]
        
        doc = self.response.lxml_etree
        password_name = owebunit.utils.xpath_first_check(doc, '//input[@type="password"]').attrib['name']
        
        params = {
            'username': 'morpheus',
            password_name: 'morpheus',
        }
        
        params = owebunit.extend_params(form.params.list, params)
        self.post(form.computed_action, body=params)
        self.assert_successish()
        
        assert 'You have successfully authenticated' in self.response.body
        
        doc = self.response.lxml_etree
        acp_link = owebunit.utils.xpath_first_check(doc, '//div[@class="copyright"]//a[text() = "Administration Control Panel"]').attrib['href']
        # note: uses previous page's form's computed action
        acp_link = urlparse.urljoin(form.computed_action, acp_link)
        
        self.get(acp_link)
        self.assert_successish()
        
        assert 'Board statistics' in self.response.body
    
    def test_acp_login_via_helper(self):
        self.login('morpheus', 'morpheus')
        self.acp_login('morpheus', 'morpheus')
        
        self.get_with_sid('/adm/index.php')
        self.assert_successish()
        
        assert 'Board statistics' in self.response.body

if __name__ == '__main__':
    import unittest
    unittest.main()