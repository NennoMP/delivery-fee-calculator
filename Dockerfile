#
# Docker file for Delivery Fee Calculator v1.0
#

FROM python:3.9-slim-buster
LABEL maintainer="matteo_pinna"
LABEL version="1.0"
LABEL description="Delivery Fee Calculator Service"

# Creating environment
COPY . /app
# Setting workdir
WORKDIR /app

# Installing all requirements
RUN ["pip", "install", "-r", "requirements.txt"]

# Environment variables
ENV FLASK_APP=monolith
ENV FLASK_ENV=development
ENV FLASK_DEBUG=false

# Expose port
EXPOSE 5000

# Command
CMD ["flask", "run", "--host", "0.0.0.0"]