import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from .validation.email_format_validator import validate_email_format
from .validation.domain_verifier import validate_domain
from .validation.smtp_checker import verify_email_exists
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['FLASK_RUN_PORT'] = os.getenv('FLASK_RUN_PORT', 5000)
app.config['FROM_EMAIL'] = os.getenv('FROM_EMAIL', 'default-from@email.com')
app.debug = os.getenv('FLASK_DEBUG', '0') == '1'


@app.route('/validate_email', methods=['POST'])
def validate_email():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({'error': 'No email provided'}), 400

        if not validate_email_format(email):
            return jsonify({'valid': False, 'reason': 'Invalid email format'}), 200

        if not validate_domain(email):
            return jsonify({'valid': False, 'reason': 'Invalid email domain'}), 200

        if not verify_email_exists(email, app.config['FROM_EMAIL']):
            return jsonify({'valid': False, 'reason': 'Email does not exist'}), 200
    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'valid': True, 'reason': 'Email is valid'}), 200
