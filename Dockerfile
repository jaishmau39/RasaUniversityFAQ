FROM python:3.7.6-stretch AS BASE

# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:3.2.0

# Use subdirectory as working directory
WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
COPY ./actions /app/actions
COPY ./models /app/models/
COPY ./actions /app/actions/
COPY ./data /app/data/
COPY ./domain.yml /app/
COPY ./config.yml /app/
COPY ./ApplicationDeadlines.csv /app/
COPY ./Calender_2022.xlsx /app/
COPY ./cs_faculty.csv /app/
COPY ./db.py /app/

# By best practices, don't run the code with root user
USER 1001