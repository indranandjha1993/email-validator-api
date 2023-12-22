import smtplib
import unittest
from unittest.mock import patch, Mock

import dns

from app.validation.smtp_checker import get_mx_record, verify_email_exists


class TestEmailVerifier(unittest.TestCase):

    @patch('dns.resolver.resolve')
    def test_get_mx_record_success(self, mock_resolve):
        mock_resolve.return_value = [Mock(exchange='mx.example.com', preference=10)]
        self.assertEqual(get_mx_record("example.com"), "mx.example.com")

    @patch('dns.resolver.resolve')
    def test_get_mx_record_no_answer(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NoAnswer()
        self.assertIsNone(get_mx_record("example.com"))

    @patch('dns.resolver.resolve')
    def test_get_mx_record_nxdomain(self, mock_resolve):
        mock_resolve.side_effect = dns.resolver.NXDOMAIN()
        self.assertIsNone(get_mx_record("example.com"))

    @patch('dns.resolver.resolve')
    def test_get_mx_record_timeout(self, mock_resolve):
        mock_resolve.side_effect = dns.exception.Timeout()
        self.assertIsNone(get_mx_record("example.com"))

    @patch('smtplib.SMTP')
    def test_verify_email_exists_failure(self, mock_smtp):
        mock_server = Mock()
        mock_server.rcpt.return_value = (550, 'Requested action not taken: mailbox unavailable')
        mock_smtp.return_value = mock_server
        self.assertFalse(verify_email_exists("user@example.com"))

    @patch('smtplib.SMTP')
    def test_verify_email_exists_exception(self, mock_smtp):
        mock_smtp.side_effect = smtplib.SMTPConnectError(421, 'Service not available')
        self.assertFalse(verify_email_exists("user@example.com"))


if __name__ == '__main__':
    unittest.main()
