import unittest


class TestExpiringCertsConfig(unittest.TestCase):

    def test_expiring_certs_config_loads_correctly(self):
        import expiring_certs_config

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpiringCertsConfig)
    unittest.TextTestRunner(verbosity=0).run(suite)
