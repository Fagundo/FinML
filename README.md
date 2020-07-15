# FinML
#### Financial Machine Learning Operations

A respository for experimentation in generating a machine learning operations (MLOps) project for the continuous integreation, continuous delivery (CI/CD) of machine learning models related to financial data.

## What on earth?
FinML hosts a number of services that aggregate into a financial analytics tool. In its current form, users can apply machine learning to near real-time (updated every minute) stock data via a Jupyter Hub. Django queries data every minute with ansynchronous Celery tasks and stores the stock quotes in a Postgres container. We host all of this in an AWS EC2 instance that provides a CI/CD pipeline via Jenkins.

## End Goal
A Machine Learning Operations pipeline that updates and deploys models based on real time data. We aim to generate price predicitons for a reinforcement learning trading agent to autonomously trade on.

## How To
You will need to copy `.env-sample` to `.env` in your local environment.
Please note that the `.env-sample` lacks the token for IEX Cloud. You will need to generate your own.

### RUN
#### AWS
`docker-compose -f docker-compose-aws.yml up`

### Add Equity to Track
#### Add S&P
Once docker containers are running, you can add S&P 500 assets to the EquityIndex with `docker exec <finml-container-tag> python3 manage.py add_sp`

#### Add Individual Equities
Navigate to `localhost:8000/equityindex` to add equities to track.
