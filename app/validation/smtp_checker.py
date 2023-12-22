import smtplib
import dns.resolver
import socket


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
        return False

    try:
        server = smtplib.SMTP(mx_record, timeout=10)
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail(from_email)
        code, message = server.rcpt(str(email))
        server.quit()

        if code == 250:
            return True
        else:
            return False
    except (socket.gaierror, socket.timeout, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError):
        return False
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False
