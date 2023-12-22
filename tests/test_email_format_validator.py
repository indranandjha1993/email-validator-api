import unittest
from app.validation.email_format_validator import validate_email_format


class TestEmailFormatValidator(unittest.TestCase):

    def test_valid_email_formats(self):
        valid_emails = [
            "email@example.com",
            "firstname.lastname@example.com",
            "email@subdomain.example.com",
            "firstname+lastname@example.com",
            "1234567890@example.com",
            "email@example-one.com",
            "_______@example.com",
            "email@example.name",
            "email@example.co.jp",
            "firstname-lastname@example.com"
        ]

        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(validate_email_format(email))

    def test_invalid_email_formats(self):
        invalid_emails = [
            "plainaddress",
            "@no-local-part.com",
            "Outlook Contact <outlook-contact@domain.com>",
            "no-at-sign.net",
            "no-tld@domain",
            ";beginning-semicolon@semicolon.com",
            "middle-semicolon@domain.co;m",
            "trailing-semicolon@domain.com;",
            "\"email-with-double-quotes@example.com\"",
            "username@example.com@example.com",
            ".email-with-leading-dot@domain.com",
            "email-with-tailing-dot@domain.com.",
            "email..with..multiple..dots@domain.com",
            "あいうえお@example.com"
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(validate_email_format(email))


if __name__ == '__main__':
    unittest.main()
