FROM python:3.7.6-stretch AS BASE

# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:3.2.0

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install pandas==1.3.5
RUN pip install facebook-scraper==0.2.59
RUN pip install gensim==4.2.0



# Copy actions folder to working directory
COPY ./actions.py /app/actions/
COPY ./ApplicationDeadlines.csv /app/
COPY ./Calender_2022.xlsx /app/
COPY ./cs_faculty.csv /app/
COPY ./db.py /app/

# By best practices, don't run the code with root user
USER 1001