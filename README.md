# Email Validation API

## Overview
This project is a Flask-based API designed to validate email addresses. It checks the email format, domain, and SMTP existence.

## Features
- **Format Validation**: Validates the email format using regular expressions.
- **Domain Verification**: Verifies the email domain via DNS lookups for MX records.
- **Existence Check**: Confirms email address existence using SMTP.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the Repository**

    ```bash
    git clone git@github.com:indranandjha1993/email-validator-api.git
    ```

2. **Navigate to Project Directory**

    ```bash
    cd email-validator-api
    ```

3. **Create and Activate Virtual Environment**

    - For Unix or MacOS:

      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - For Windows:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Environment Setup**

    Create a `.env` file in the root directory with the following content:

    ```
    FLASK_APP=server.py
    FLASK_ENV=development
    FLASK_RUN_PORT=5000
    FROM_EMAIL=your-email@example.com
    ```

### Running the Application

- Start the server using Flask:

    ```bash
    flask run
    ```

  Or directly with Python:

    ```bash
    python server.py
    ```

  The API will be available at `http://localhost:5000`.

## Usage

Send a `POST` request to `/validate_email` with a JSON payload:

```json
{
    "email": "test@example.com"
}
```

### Response structure:

```json
{
    "valid": true | false,
    "reason": "Email is valid" | "Reason for invalidation"
}
```

## Testing
To run unit tests, execute:

```shell
python -m unittest discover -s tests
```