import pymangal
import sys
import unittest
from jsonschema import validate, ValidationError

from pymangal import api
from pymangal import makeschema

class api_test(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://mangal.uqar.ca'

    def test_trailing_slash(self):
        assert api.mangal(url=self.base_url+'/').root == self.base_url
    
    def test_suffix_no_slash(self):
        assert api.mangal(url=self.base_url, suffix='api/v1').root == self.base_url
    
    def test_suffix_no_leading_slash(self):
        assert api.mangal(url=self.base_url, suffix='api/v1/').root == self.base_url
    
    def test_suffix_no_trailing_slash(self):
        assert api.mangal(url=self.base_url, suffix='/api/v1').root == self.base_url

    def test_URL_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(url = 4))

    def test_Fake_URLs_give_404(self):
        self.assertRaises(ValueError, lambda : api.mangal(url = 'http://t.co/'))

    def test_if_usr_then_pwd(self):
        self.assertRaises(ValueError, lambda : api.mangal(usr = 'test'))

    def test_if_pwd_then_usr(self):
        self.assertRaises(ValueError, lambda : api.mangal(pwd = 'test'))

    def test_usr_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr = 4, pwd = 'test'))

    def test_pwd_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr = 'test', pwd = 4))

    def test_minimal_elements_in_resources(self):
        mg = api.mangal()
        assert 'taxa' in mg.resources
        assert 'dataset' in mg.resources
        assert 'network' in mg.resources
        assert 'interaction' in mg.resources

    def test_allowed_verbs(self):
        mg = api.mangal()
        for verb in ['get', 'post', 'patch']:
            assert verb in mg.verbs['taxa']


## Tests the .Post() function
class post_test(unittest.TestCase):

    def setUp(self):
        self.mg = api.mangal()
        self.mg_auth = api.mangal(usr='test', pwd='test')
    
    def test_no_auth(self):
        self.assertRaises(ValueError, lambda : self.mg.Post())

    def test_no_data(self):
        self.assertRaises(ValueError, lambda : self.mg_auth.Post())

    def test_string_data(self):
        self.assertRaises(TypeError, lambda : self.mg_auth.Post(data = 'name: test'))

    def test_bad_data(self):
        self.assertRaises(ValidationError, lambda : self.mg_auth.Post(resource='taxa', data = {'taxa': 'taxa name'}))

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg_auth.Post(resource=4, data = {}))
    
    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg_auth.Post(resource='TAXA', data = {}))

## Tests the .Get() function
class get_test(unittest.TestCase):

    def setUp(self):
        self.mg = api.mangal()

    def test_weird_id_type(self):
        self.assertRaises(TypeError, lambda : self.mg.Get(key = [1, 2]))

    def test_id_0_is_404(self):
        self.assertRaises(ValueError, lambda : self.mg.Get(key='0'))

    def test_id_int_is_ok(self):
        assert isinstance(self.mg.Get(key=1), dict)
    
    def test_output_dict(self):
        assert isinstance(self.mg.Get(key='1'), dict)

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.Get(resource=4))
    
    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg.Get(resource='TAXA'))


## Tests the .List() function
class list_test(unittest.TestCase):

    def setUp(self):
        self.mg = api.mangal()

    def test_autopage_is_boolean(self):
        self.assertRaises(TypeError, lambda : self.mg.List(autopage=1))

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List(4))

    def test_filters_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List('taxa', 2))

    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg.List('TAXA'))

    def test_output_list(self):
        assert isinstance(self.mg.List('taxa'), list)

## Tests the makeschema function
class makeschema_test(unittest.TestCase):

    def test_wrong_title(self):
        self.assertRaises(TypeError, lambda : makeschema({}, 'name', 4))

    def test_no_name(self):
        self.assertRaises(ValueError, lambda : makeschema({}, None, 'description'))
    
    def test_name_no_str(self):
        self.assertRaises(TypeError, lambda : makeschema({}, 4, 'description'))
    
    def test_wrong_data_format(self):
        self.assertRaises(TypeError, lambda : makeschema([], 'name', 'description'))

def main():
    if sys.version_info[1] < 7 :
        unittest.main()
    else :
        unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
