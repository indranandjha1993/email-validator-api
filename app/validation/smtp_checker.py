import smtplib
import dns.resolver
import socket

from flask import current_app


def get_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = sorted(records, key=lambda record: record.preference)[0]
        return str(mx_record.exchange).rstrip('.')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return None


def verify_email_exists(email, from_email):
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    if not mx_record:
        current_app.logger.info(f"No MX record found for domain: {domain}")
        return False

    try:
        server = smtplib.SMTP(mx_record, timeout=10)
        server.set_debuglevel(1)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail(from_email)
        code, message = server.rcpt(str(email))
        server.quit()

        if code == 250:
            current_app.logger.info(f"Email address {email} exists.")
            return True
        else:
            current_app.logger.info(f"Email address {email} does not exist. SMTP response code: {code}")
            return False
    except (socket.gaierror, socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
        current_app.logger.error(f"SMTP connection error for email {email}: {e}")
        return False
    except Exception as e:
        current_app.logger.error(f"Unexpected error during SMTP verification for email {email}: {e}")
        return False
