# Vendor Management System

The Vendor Management System is a Django-based web application designed to manage vendor profiles, purchase orders, and historical performance metrics.

## Features

- Vendor Profile Management
- Purchase Order Management
- Historical Performance Tracking
- RESTful API for integration

## Requirements

- Python 3.x
- Django 3.x
- Other dependencies (see `requirements.txt`)

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/vendor-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd vendor-management-system
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate  # On Windows
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Run migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser account (for admin access):

    ```bash
    python manage.py createsuperuser
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Open the application in your browser: [http://localhost:8000/](http://localhost:8000/)

## API Documentation

Explore the API using Swagger or ReDoc:

- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).

