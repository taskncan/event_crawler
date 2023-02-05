## Introduction

This is a Dockerfile for a Python web scraping project that extracts event information from the Lucerne Festival website and stores the data in a PostgreSQL database.

## Requirements
The following software and packages are required to build and run this project:

* Docker
* Python 3.10
* PostgreSQL

## Usage
To build the Docker image, run the following command in the same directory as the Dockerfile:
```
docker build -t event_crawler .
```
To run the Docker container, use the following command:
```
docker run --name event_crawler -e POSTGRES_HOST=host.docker.internal -e POSTGRES_PORT=5432 -e POSTGRES_DB=event_crawler -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=331gfa event_crawler
```
Note: Replace the values for the environment variables POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD with the appropriate values for your PostgreSQL setup.

## Limitations
This project has the following limitations:

The code only scrapes events from the Lucerne Festival website and stores the data in a PostgreSQL database.
The code only works with the specific HTML structure of the Lucerne Festival website and may not work with other websites.

## Conclusion
This project demonstrates a basic example of web scraping and how to store the data in a PostgreSQL database using Python and Docker.
