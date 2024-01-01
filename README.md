# fastapi_quickstart_docker

A basic framework for a project using fastapi with postgresql db with docker

# How to run

1. setting up environment:
    - create .env.prod, .env.dev and .env.test files in the environment directory
    - copy the content of .env.example to each of the files
    - change the values of the variables in the files to your own values
2. starting database containers:
    - run `docker compose -f docker-compose.yml start db_test db_main`
    - or use Services tab if using pycharm pro
    - make sure that you have correct plugin installed for
      docker-compose: https://docs.docker.com/compose/install/linux/#install-using-the-repository
    - if for whatever reason you're unable to use docker-compose, you can set up the database manually or using docker
      desktop
3. starting the app:
    - to run tests, after making sure that you have established connections with relevant databases, and have set up all
      necessary env variables, run `pytest tests` in the terminal from within main project directory
    - to run project use run_project.py script in run directory
    - you can also start the API manually by using uvicorn run:app with appropriate arguments in the terminal from
      within main project directory
