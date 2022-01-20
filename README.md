# Wolt Summer 2022 Software Engineering Internship (Backend)

[![CircleCI](https://circleci.com/gh/NennoMP/delivery-fee-calculator.svg?style=svg)](https://app.circleci.com/pipelines/github/NennoMP/delivery-fee-calculator)
[![codecov](https://codecov.io/gh/NennoMP/delivery-fee-calculator/branch/main/graph/badge.svg?token=STRMRZLL8T)](https://codecov.io/gh/NennoMP/delivery-fee-calculator)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

## Overview
The application is implemented with a monolith-based architecture, since it is not complex enough for a microservice-based one, is completely Dockerized and PEP8 compliant.

In order to create OpenAPI documentation for the APIs, Swagger and Connexion framework were used. The application should be running on **localhost:5000 (127.0.0.1:5000)** and the Swagger interface, which allows to analyze and test the endpoints simply from the web-browser, can be accessed at **localhost:5000/ui (127.0.0.1:5000/ui)**.

Some **CI/CD tools (CircleCI, Codecov)** were used in order to build and test the project, as can be seen from the above badges, and, from a security point of view, the application was tested with **Bandit** (static vulnerabilities' analysis).

### Settings
Static data related to the application is stored in the configuation file `settings.json`.
```json
{
    "delivery_fees": {
        "min_order_no_surcharge": 1000,
        "min_order_free_delivery": 10000,
        "distance_block_size": 500,
        "distance_fee": 100,
        "n_items_fee_free": 4,
        "item_fee": 50,
        "max_fee": 1500
    },
    "special_rush": {
        "weekday": 4,
        "start_time": 15,
        "end_time": 19,
        "multiplier": 1.1
    }
}
```

### APIs
For what concern data validation, the `marshmallow` library was used in order to define schemas/models (`models/delivery_order.py`). I assumed that the input parameters that were integers could not be negative (trivial) and not equal to 0, and that the order datetime could not be in the past.

I would've added rate limiting and payload size limits in order to prevent possible DoS and brute force attacks. However, I thought this could be a bit overkill for this assignment and I decided to not implement them, since they were not requirements.

## Instructions
You can decide to test/run the application with or without Docker, notice that if you're on Windows you **MUST** run the application with Docker (since `time.tzset()` is available only on Unix).
Below you can find a short tutorial for both approaches.
### Run the application (Docker version)

If you want to run the application with Docker, make sure you have Docker Desktop running (if you are on Windows) and follow these steps:

1. Go on the project's root
2. Build the project with `docker-compose build`
3. Run the application with `docker-compose up`

### Run the application (Script version)

If you want to run the application without Docker, you have to follow these steps:

1. Go on the project's root
2. Create a virtual environment with `virtualenv venv`
3. Activate it with `source venv/bin/activate` or `source venv/scripts/activate`
4. Install all requirements needed with `pip install -r requirements.txt`
5. Run the script `run.sh` with `bash run.sh`

### Testing the application
The application is already tested with CI/CD tools. However, if you would like to manually run the application's tests, follow the steps below.

If you have not yet created a virtual environment and installed the requirements:
1. Go on the project's root
2. Create a virtual environment with `virtualenv venv`
3. Activate it with `source venv/bin/activate` or `source venv/scripts/activate`
4. Install all requirements needed with `pip install -r requirements.txt`

Now simply execute the `pytest` command. The testing is set to fail if the coverage is not above 90%.
