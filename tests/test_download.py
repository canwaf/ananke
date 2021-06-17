from ananke.download import get_endpoint
import unittest
import nose2
import ananke

class TestEndPoint(unittest.TestCase):

    def test_get_endpoint(self):
        self.assertEqual(get_endpoint(), "https://staging.gss-data.org.uk/sparql")

if __name__ == '__main__':
    unittest.main()