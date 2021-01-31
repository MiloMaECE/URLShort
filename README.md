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



By default, when the server starts, the user `testuser` with password `password` will be created for your convenience. You could also create other users using API if needed.

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

