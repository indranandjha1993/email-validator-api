import dns.resolver

from flask import current_app
import dns.resolver


def validate_domain(email):
    domain = email.split('@')[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        current_app.logger.info(f"MX record found for domain: {domain}")
        return True
    except dns.resolver.NoAnswer:
        current_app.logger.warning(f"No MX record found for domain: {domain}")
        return False
    except dns.resolver.NXDOMAIN:
        current_app.logger.warning(f"NXDOMAIN: No such domain {domain}")
        return False
    except dns.exception.Timeout:
        current_app.logger.error(f"DNS query timed out for domain {domain}")
        return False
    except Exception as e:
        current_app.logger.error(f"Unexpected error during MX record resolution for domain {domain}: {e}")
        return False
