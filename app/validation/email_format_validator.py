import re
from flask import current_app


def validate_email_format(email):
    pattern = r'^(?!\.)(?!.*\.\.)([A-Za-z0-9\._\+-]+)@([A-Za-z0-9\.-]+\.[A-Za-z]{2,})$'
    if re.match(pattern, email):
        current_app.logger.info(f"Valid email format: {email}")
        return True
    else:
        current_app.logger.warning(f"Invalid email format: {email}")
        return False
