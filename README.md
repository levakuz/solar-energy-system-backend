# Solar energy calculation system

## Backend part of solar energy calculation system

### Pre-installed requirements

- Python >= 3.11
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (If you don't want to install project's infrastructure direct on yours PC)
- MongoDB
- PostgreSQL


### Development environment

#### Project infrastructure
1. Set environment variables for development environment as shown in
"Development environment settings" in example.env file 
2. Deploy project infrastructure with docker compose
`docker compose --file docker-compose.dev.yml up -d`

#### Project environment for development

1. Install python dependencies: `poetry install`
2. If you do not use poetry, you can install dependencies from
requirements.txt: `pip install -r requirements.txt`
3. Create .env file with environment variables. 
You can find example in `example.env` file. 
4. Load environment variables from `.env` file `export $(cat .env | xargs)`
   (remove all comments in file before)
5. Update database state by using tortoise ORM aerich migration 
tool: `aerich upgrade`
6. Run the `run.py` script, which will start the 
uvicorn web server: `poetry run python run.py` or if you
use Python without poetry: `python run.py`

#### Project environment for production

1. Make sure that you have deployed infrastructure, 
namely:
 - MongoDB
 - PostgreSQL

You can deploy it with docker compose (see section Project infrastructure)

If you use infrastructure for project from 
docker-compose.dev.yml file then you need to set 
your DB_IP environment variable as name of the container
for example: DB_IP=solar-energy-system-backend_solar_energy_system_pg_1
and the same for MongoDB IP: MONGO_IP=mongo

2. Deploy docker container with web server: `docker compose --file docker-compose.prod.yml up -d --build`