import unittest
from unittest.mock import patch
import dns.resolver
from app.validation.domain_verifier import validate_domain


class TestDomainValidator(unittest.TestCase):

    @patch('dns.resolver.resolve')
    def test_valid_domain(self, mock_resolve):
        mock_resolve.return_value = None
        self.assertTrue(validate_domain("user@example.com"))

    @patch('dns.resolver.resolve')
    def test_invalid_domain(self, mock_resolve):
        """
        Test that an invalid domain is correctly identified.
        """
        mock_resolve.side_effect = dns.resolver.NXDOMAIN()
        self.assertFalse(validate_domain("user@nonexistentdomain.com"))

    @patch('dns.resolver.resolve')
    def test_domain_with_no_mx_records(self, mock_resolve):
        """
        Test that a domain without MX records is identified as invalid.
        """
        mock_resolve.side_effect = dns.resolver.NoAnswer()
        self.assertFalse(validate_domain("user@domainwithoutmx.com"))

    @patch('dns.resolver.resolve')
    def test_timeout_exception(self, mock_resolve):
        """
        Test that a timeout exception is handled properly.
        """
        mock_resolve.side_effect = dns.exception.Timeout()
        self.assertFalse(validate_domain("user@timeoutdomain.com"))


if __name__ == '__main__':
    unittest.main()
