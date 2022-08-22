# Micro warehouse

Application created to practice microservices architecture. Orders can be created, updated or allocated using docs requests. Implemented simulation of AWS SQS service using Localstack. Created with FastAPI framework.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Contact](#contact)

## Technologies
* Python version: 3.8.10
* FastAPI version: 0.75.1
* Docker version: 19.03.8

## Setup
To build backend locally:
```
make build
```

To start backend locally:
```
make up
```

To run tests:
```
make test app=allocation
```
or
```
make test app=storage
```

For docs of allocation service:
```
http://localhost:8000/docs
```

For docs of storage service:
```
http://localhost:8001/docs
```

## Contact
Created by Adam Misiak