# Project Name: User Registration and Login System

This project provides an API for user registration and login with JWT authentication. Users can register with their phone number, password, and membership type (Silver, Gold, Diamond). After registration, they can log in to receive JWT tokens for secure authentication.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git

2. Create a virtual environment
   ```bash
   python -m venv venv

3. Activate the virtual environment
   ```bash
   venv\Scripts\activate

4. Install dependencies from the requirements.txt file
   ```bash
   pip install -r requirements.txt


## API Endpoints

1. User Registration

    Endpoint: POST /api/register

    Description: This endpoint allows users to register with their phone number, password, and membership type.

    Request Body:
    ```bash
    {
    "phone_number": "98xxxxxxxx",
    "password": "123",
    "membership_type": "Diamond"
    }


2. User Login

    Endpoint: POST /api/login

    Description: This endpoint allows users to login with their username and password to receive JWT tokens.

    Request Body:

    ```bash
    {
    "phone_number": "98xxxxxxxx",
    "password": "123"
    }
