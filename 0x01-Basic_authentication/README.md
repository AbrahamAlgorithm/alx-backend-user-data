# 0x01. Basic authentication
- Back-end
- Authentification

This project provides a simple API with a user model. The API is built using Flask and handles user data storage via serialization/deserialization in files.

## Setup

1. Install the required Python packages:

    ```bash
    pip3 install -r requirements.txt
    ```

2. Set the environment variables:

    ```bash
    export API_HOST=0.0.0.0
    export API_PORT=5000
    ```

3. Start the API server:

    ```bash
    python3 -m api.v1.app
    ```

4. Test the API:

    ```bash
    curl "http://0.0.0.0:5000/api/v1/status" -vvv
    ```

## Code Style

Ensure your code follows the `pycodestyle` guidelines (version 2.5).

## Documentation

All modules, classes, and functions should include documentation explaining their purpose.

