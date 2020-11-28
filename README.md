# URL-Shortener

A RESTful API server providing URL-shortener service .

## How To Start

1. Build the docker image.
   
   ```
   docker-compose build
   ```

2. Run the server
   
   ```
   docker-compose up
   ```

The app server will start and user could use it by`http://localhost:5000/` on the docker host. The PORT `5000` of the container will be mapped to PORT `5000` on the docker host.

## API DOCUMENTATION

All API descriptions could be found in the API doc built by Swagger. All API calls could also be tested here.



By default, when the server starts, the user `gamehive` with password `gamehive`will be created for your convenience. You could also create other users using API if needed.

```
http://localhost:5000/apidocs/
```

## Technology Stack

- Python

- Flask

- PostgreSql 

- SQLAlchemy

- JWT

- Swagger

- Docker && Docker-Compose

## About Me

I'm Yunlong Ma, earned a master's degree in Electrical and Computer Engineering in 2019 March. I've built and trained several deep learning models for image processing using Python in my master. Then I joined Lumen as a backend developer in 2019 March after graduation. I'm mainly respoinsible for developing RESTful APIs to analyze the sales data for our clients using Node.Js and MongoDB. Then I developed and trained several deep learning models in Python to further study the sales data and built a Python Flask API server to integrate with our production environment in Node.JS. Deep learning models did improve the analysis results. 

So sorry for the delay to deliver this task. I had unexpected some personal things to do this week and had to deliver a new feature development in Lumen. Because I didn't touch the SQL databases before(using MongoDB instead), I spent some time to learn some basics about PostgreSql. I could learn PostgreSql if needed. 
