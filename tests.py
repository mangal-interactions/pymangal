import pymangal
import sys, os
import unittest
from jsonschema import validate, ValidationError
import requests as re

from pymangal import api
from pymangal import makeschema
from pymangal import checks
import pymangal.helpers as helpers

class api_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')

    def test_trailing_slash(self):
        assert api.mangal(url=self.url+'/').root == self.url

    def test_suffix_no_slash(self):
        assert api.mangal(url=self.url, suffix='api/v1').root == self.url

    def test_suffix_no_leading_slash(self):
        assert api.mangal(url=self.url, suffix='api/v1/').root == self.url

    def test_suffix_no_trailing_slash(self):
        assert api.mangal(url=self.url, suffix='/api/v1').root == self.url

    def test_URL_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(url=4))

    def test_fake_URLs_give_404(self):
        self.assertRaises(ValueError, lambda : api.mangal(url='http://t.co/'))

    def test_if_usr_then_key(self):
        self.assertRaises(ValueError, lambda : api.mangal(usr=self.usr))

    def test_if_key_then_usr(self):
        self.assertRaises(ValueError, lambda : api.mangal(key=self.key))

    def test_usr_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr=4, key=self.key))

    def test_key_is_a_string(self):
        self.assertRaises(TypeError, lambda : api.mangal(usr=self.usr, key=4))

    def test_correct_username(self):
        self.assertRaises(ValueError, lambda : api.mangal(usr='user', key=self.key))

    def test_minimal_elements_in_resources(self):
        mg = api.mangal()
        assert 'taxa' in mg.resources
        assert 'dataset' in mg.resources
        assert 'network' in mg.resources
        assert 'interaction' in mg.resources

    def test_allowed_verbs(self):
        mg = api.mangal(url=self.url)
        for verb in ['get', 'post', 'patch']:
            assert verb in mg.verbs['taxa']

## Tests the check functions
class check_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)

    def test_check_res_bad_api(self):
        self.assertRaises(TypeError, lambda : checks.check_resource_arg(self.url, 'taxa'))

    def test_check_res_no_str(self):
        self.assertRaises(TypeError, lambda : checks.check_resource_arg(self.mg, 4))

    def test_check_res_no_res(self):
        self.assertRaises(ValueError, lambda : checks.check_resource_arg(self.mg, 'taxon'))

## Tests the .Post() function
class post_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)
        self.mg_auth = api.mangal(self.url, usr=self.usr, key=self.key)
        self.taxa = {'name': 'Carcharodon carcharias', 'vernacular': 'Great white shark', 'eol': 213726, 'status': 'confirmed'}

    def test_str_representation(self):
        assert self.mg.__str__() == '---------------------------\nMangal API connector\nURL: ' + self.url

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

    def test_send_good_taxa(self):
        ccarc = self.mg_auth.Post('taxa', self.taxa)
        assert type(ccarc['id']) is int
        assert ccarc['name'] == self.taxa['name']
        re.delete(self.mg_auth.root + ccarc['resource_uri'])

    def test_send_duplicate_taxa(self):
        ccarc = self.mg_auth.Post('taxa', self.taxa)
        self.assertRaises(ValueError, lambda : self.mg_auth.Post('taxa', self.taxa))
        re.delete(self.mg_auth.root + ccarc['resource_uri'])

## Tests the .Patch() function
class patch_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)
        self.mg_auth = api.mangal(self.url, usr=self.usr, key=self.key)
        self.taxa = {'name': 'Carcharodon carcharias', 'vernacular': 'Great white shark', 'status': 'confirmed'}
        self.eol = 213726

    def test_patch_taxa(self):
        ccarc = self.mg_auth.Post('taxa', self.taxa)
        ccarc['eol'] = self.eol
        ccarc = self.mg_auth.Patch('taxa', ccarc)
        assert ccarc['eol'] == self.eol
        re.delete(self.mg_auth.root + ccarc['resource_uri'])

    def test_patch_taxa_if_no_uri(self):
        ccarc = self.mg_auth.Post('taxa', self.taxa)
        ccarc['eol'] = self.eol
        ccarc.pop('resource_uri', None)
        ccarc = self.mg_auth.Patch('taxa', ccarc)
        assert ccarc['eol'] == self.eol
        re.delete(self.mg_auth.root + ccarc['resource_uri'])

## Tests the .Get() function
class get_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)
        self.mg_auth = api.mangal(self.url, usr=self.usr, key=self.key)

    def test_weird_id_type(self):
        self.assertRaises(TypeError, lambda : self.mg.Get(key = [1, 2]))

    def test_id_0_is_404(self):
        self.assertRaises(ValueError, lambda : self.mg.Get(key='0'))

    def test_id_int_is_ok(self):
        dummy_taxa = self.mg_auth.Post('taxa', {'name': 'dummy', 'status': 'trophic species'})
        assert isinstance(self.mg.Get('taxa', dummy_taxa['id']), dict)
        re.delete(self.mg_auth.root + dummy_taxa['resource_uri'])

    def test_id_str_is_ok(self):
        dummy_taxa = self.mg_auth.Post('taxa', {'name': 'dummy', 'status': 'trophic species'})
        assert isinstance(self.mg.Get('taxa', str(dummy_taxa['id'])), dict)
        re.delete(self.mg_auth.root + dummy_taxa['resource_uri'])

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.Get(resource=4))

    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg.Get(resource='TAXA'))

## Tests the .List() function
class list_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)
        self.mg_auth = api.mangal(self.url, usr=self.usr, key=self.key)

    def test_resource_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List(4))

    def test_filters_is_str(self):
        self.assertRaises(TypeError, lambda : self.mg.List('taxa', 2))

    def test_filters_space_replaced(self):
        assert isinstance(self.mg.List('taxa', 'name__contains=s b'), dict)

    def test_filters_valid_relationship(self):
        self.assertRaises(ValueError, lambda : self.mg.List('taxa', 'name__islike=Lame'))

    def test_filters_valid_structure(self):
        self.assertRaises(ValueError, lambda : self.mg.List('taxa', 'name__contains=a&name_endswith=s'))

    def test_filters_multiple(self):
        assert isinstance(self.mg.List('taxa', 'name__contains=a&name__endswith=s'), dict)

    def test_filters_has_equal_sign(self):
        self.assertRaises(ValueError, lambda : self.mg.List('taxa', 'name__contains_i'))

    def test_resource_available(self):
        self.assertRaises(ValueError, lambda : self.mg.List('TAXA'))

    def test_output_list(self):
        assert isinstance(self.mg.List('taxa'), dict)

    def test_offset_list(self):
        assert isinstance(self.mg.List('taxa', offset=1), dict)

    def test_page_list(self):
        obj = [self.mg_auth.Post('taxa', {'name': 'dummy'+str(i), 'status': 'confirmed'}) for i in xrange(5)]
        assert len(self.mg.List('taxa', page=4)['objects']) == 4
        for o in obj:
            re.delete(self.mg_auth.root + o['resource_uri'])

    def test_page_offset_list(self):
        obj = [self.mg_auth.Post('taxa', {'name': 'dummy'+str(i), 'status': 'confirmed'}) for i in xrange(5)]
        assert isinstance(self.mg.List('taxa', offset=1, page=3)['objects'], list)
        for o in obj:
            re.delete(self.mg_auth.root + o['resource_uri'])

    def test_page_all(self):
        obj = [self.mg_auth.Post('taxa', {'name': 'dummy'+str(i), 'status': 'confirmed'}) for i in xrange(50)]
        assert isinstance(self.mg.List('dataset', page='all')['objects'], list)
        for o in obj:
            re.delete(self.mg_auth.root + o['resource_uri'])

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

# Tests the makeschema function
class makeschema_test(unittest.TestCase):

    def test_wrong_title(self):
        self.assertRaises(TypeError, lambda : makeschema({}, 'name', 4))

    def test_no_name(self):
        self.assertRaises(ValueError, lambda : makeschema({}, None, 'description'))

    def test_name_no_str(self):
        self.assertRaises(TypeError, lambda : makeschema({}, 4, 'description'))

    def test_wrong_data_format(self):
        self.assertRaises(TypeError, lambda : makeschema([], 'name', 'description'))

# Tests the helpers
class helpers_test(unittest.TestCase):

    def setUp(self):
        self.url = os.environ.get('mg_test_url','http://mangal.io:8080')
        self.usr = os.environ.get('mg_test_usr','test')
        self.key = os.environ.get('mg_test_key','9d00823baa5be60d788d079143d9785a4ffd3eec')
        self.mg = api.mangal(self.url)

    def test_uri_from_username(self):
        assert helpers.uri_from_username(self.mg, 'test') == '/api/v1/user/1/'

    def test_uri_from_username_with_no_user(self):
        self.assertRaises(ValueError, lambda : helpers.uri_from_username(self.mg, 'NoSuchUser'))

    def test_uri_from_username_wants_str(self):
        self.assertRaises(TypeError, lambda : helpers.uri_from_username(self.mg, 4))


def main():
    URL = 'http://mangal.io:8080'
    if len(sys.argv) > 1:
        for i in range(len(sys.argv)-1):
            if sys.argv[i] in ['-h', '--host']:
                if sys.argv[i+1] == 'local':
                    URL = "http://127.0.0.1:8000"
                else:
                    URL = sys.argv[i+1]
                del(sys.argv[i+1])
                del(sys.argv[i])
    print "Testing on host "+URL+"\n"
    USER = 'test'
    KEY = '9d00823baa5be60d788d079143d9785a4ffd3eec'
    ## Cleaning DB
    mg = api.mangal(URL, usr=USER, key=KEY)
    re.delete(mg.root + '/api/v1/taxa/')
    ##
    os.environ['mg_test_url'] = URL
    os.environ['mg_test_usr'] = USER
    os.environ['mg_test_key'] = KEY
    if sys.version_info[1] < 7 :
        unittest.main()
    else :
        unittest.main(verbosity=1)

if __name__ == '__main__':
    main()
