# Getting Started

- Clone the repo to your local device `git clone git@github.com:BFT-Smartbus/smartbus-heartbeat.git`

## Setting up Python virtual environment

1. Set up a virtual environment in root folder: `python3 -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install libraries: `pip3 install -r requirements.txt`
4. Run `deactivate` to close the virtual environment.

## Creating the database

1. Run `psql` in your terminal
2. Create a database called _heartbeat_ by running `CREATE DATABASE heartbeat`
3. Create a username and secure password `CREATE USER <username> WITH PASSWORD <password>`
4. Grant user admin privileges `GRANT ALL PRIVILEGES ON DATABASE heartbeat TO <username>`

_Note the username and password as you will need them for setting up environmet variables_.

## Setting up .env file

1. Make a copy `env.example` and rename it to `.env`
2. Change USERNAME and PASSWORD to match the username and password from the previous step

## Generating the tables

In the root folder, run `flask run` to create heartbeat tables
