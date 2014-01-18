import pymangal
import unittest

from pymangal import api

class api_test(unittest.TestCase):

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


def main():
    unittest.main()

if __name__ == '__main__':
    main()
