# Wolt Summer 2022 Software Engineering Internship (Backend)

## Instructions
In order to create OpenAPI specification for the API endpoints, Swagger and Connexion were used. The Swagger interface, which allows to analyze and test the endpoints simply from a web-browser, can be accessed with **/ui**. The application should be running on **localhost (127.0.0.1:5000)**.

You can decide to test/run the application with or without Docker, below you can find the steps for both approaches.

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