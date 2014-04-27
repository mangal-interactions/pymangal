import pymangal
import sys
import unittest
from jsonschema import validate, ValidationError

from pymangal import api
from pymangal import makeschema
from pymangal import checks

# These are testing user informations
# Anything written by this user will be destroyed
USER = 'test_user'
KEY = '2ab887fd3857bdfb1de9d80999a89a4dd57a1292'

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
        self.assertRaises(TypeError, lambda : api.mangal(url=4))

    def test_Fake_URLs_give_404(self):
        self.assertRaises(ValueError, lambda : api.mangal(url='http://t.co/'))

    def test_if_usr_then_key(self):
        self.assertRaises(ValueError, lambda : api.mangal(usr=USER))

    def test_if_key_then_usr(self):
        self.assertRaises(ValueError, lambda : api.mangal(key=KEY))

    def test_usr_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr=4, key=KEY))

    def test_key_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr=USER, key=4))

    def test_correct_username(self):
        self.assertRaises(ValueError, lambda : api.mangal(usr='user', key=KEY))

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

## Tests the check functions
class check_test(unittest.TestCase):

    def setUp(self):
        self.mg = api.mangal()

    def test_check_res_bad_api(self):
        self.assertRaises(TypeError, lambda : checks.check_resource_arg('http://mangal.uqar.ca', 'taxa'))

    def test_check_res_no_str(self):
        self.assertRaises(TypeError, lambda : checks.check_resource_arg(self.mg, 4))

    def test_check_res_no_res(self):
        self.assertRaises(ValueError, lambda : checks.check_resource_arg(self.mg, 'taxon'))


## Tests the .Post() function
class post_test(unittest.TestCase):

    def setUp(self):
        self.mg = api.mangal()
        self.mg_auth = api.mangal(usr=USER, key=KEY)

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

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List(4))

    def test_filters_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List('taxa', 2))

    def test_filters_space_replaced(self):
        assert isinstance(self.mg.List('taxa', 'name__contains=s b'), dict)

    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg.List('TAXA'))

    def test_output_list(self):
        assert isinstance(self.mg.List('taxa'), dict)

    def test_offset_list(self):
        assert isinstance(self.mg.List('taxa', offset=1), dict)

    def test_page_list(self):
        assert len(self.mg.List('taxa', page=4)['objects']) <= 4

    def test_page_offset_list(self):
        assert isinstance(self.mg.List('taxa', offset=1, page=3)['objects'], list)

    def test_page_all(self):
        assert isinstance(self.mg.List('dataset', page='all')['objects'], list)

    def test_page_offset_filter(self):
        assert isinstance(self.mg.List('taxa', page=2, offset=2, filters='name__contains=i')['objects'], list)

    def test_page_badstring(self):
        self.assertRaises(ValueError, lambda : self.mg.List('dataset', page='All'))

    def test_page_badtype(self):
        self.assertRaises(TypeError, lambda : self.mg.List('dataset', page=[1,2]))

    def test_page_badvalue(self):
        self.assertRaises(ValueError, lambda : self.mg.List('dataset', page=0))

    def test_offset_badtype(self):
        self.assertRaises(TypeError, lambda : self.mg.List('dataset', offset="1"))

    def test_offset_badvalue(self):
        self.assertRaises(ValueError, lambda : self.mg.List('dataset', offset=-1))

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
