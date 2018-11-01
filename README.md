# Miner for student feedback

## Project Description

Student Feedback Surveys at Swinburne University of Technology contain both numeric (i.e. ratings) as well as textual information (“free” comments). When the university assess the teaching quality of a Unit of Study, generally, only the numerical responses are considered, and summarized, but there may be interesting and actionable information in the free text responses from students very little is currently done in a systematic way. The textual feedback is often only looked at from the perspective of a single unit of study, but not across related Units of Study. Hence, there is the potential to extract more information from
Student Feedback Surveys that will allow Unit of Study conveners, program coordinators, department chairs etc. to make better informed decisions on how to improve learning outcomes for students.

The aim of this project is to develop a software system that incorporates a number of text mining and data aggregation algorithms to enable improved qualitative and textual analysis of Student Feedback Surveys.

Students interested in this project are expected to have good analytical and programming skills, knowledge in data mining and analytics, especially mining of textual information, familiarity with basic statistics, and the willingness to explore a variety of technologies to create a solution.

## Requirements

Python 3.6.6 (for Heroku deploy),
Ubuntu 18.04,
PostgreSQL,
Redis server

## Quick Start

### First Steps

```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ export APP_SETTINGS="config.DevelopmentConfig"
$ export DATABASE_URL="[POSTGRES database url here]"
```

### Set up Migrations

```sh
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Run

Run each in a different terminal window...

```sh
# redis
$ redis-server

# worker process
$ python worker.py

# the app
$ python app.py
```
