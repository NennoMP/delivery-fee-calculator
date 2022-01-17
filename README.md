# Wolt Summer 2022 Software Engineering Internship (Backend)

[![CircleCI](https://circleci.com/gh/NennoMP/delivery-fee-calculator.svg?style=svg)](https://app.circleci.com/pipelines/github/NennoMP/delivery-fee-calculator)
[![codecov](https://codecov.io/gh/NennoMP/delivery-fee-calculator/branch/main/graph/badge.svg?token=STRMRZLL8T)](https://codecov.io/gh/NennoMP/delivery-fee-calculator)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


## Overview
In order to create OpenAPI documentation for the API endpoints, Swagger and Connexion framework were used. The Swagger interface, which allows to analyze and test the endpoints simply from the web-browser, can be accessed with **/ui**. The application should be running on **localhost:5000 (127.0.0.1:5000)**. 

Some **CI/CD tools (CircleCI, Codecov)** were used in order to build and test the project, as can be seen from the above badges, and, from a security point of view, the application was tested with **Bandit** (static vulnerabilities analysis).

You can decide to test/run the application with or without Docker, notice that if you're on Windows you **MUST** run the application with Docker (since `time.tzset()` is available only on Unix).
Below you can find a short tutorial for both approaches.
### Run the application (Docker version)

If you want to run the application with Docker, make sure you have Docker Desktop running (if you are on Windows) and follow these steps:

1. Build the project with `docker-compose build`
2. Run the application with `docker-compose up`

### Run the application (Flask version)

If you want to run the application without Docker, you have to follow these steps:

1. Create a virtual environment with `virtualenv venv`
2. Activate it with `source venv/bin/activate` or `source venv/scripts/activate`
3. Install all requirements needed with `pip install -r requirements.txt`
4. Run the script `run.sh` with `bash run.sh`
