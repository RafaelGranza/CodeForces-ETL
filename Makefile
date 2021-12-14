all:
	@echo "Commands:\n"
	@echo "   Build the dockers:"
	@echo "      make build\n"
	@echo "   Rebuild the dockers:"
	@echo "      make rebuild\n"
	@echo "   Start the dockers:"
	@echo "      make start\n"
	@echo "   Stop the dockers:"
	@echo "      make stop\n"
	@echo "   Clean the dockers:"
	@echo "      make clean\n"
	

build:
	@echo "Building CodeForces-ETL"
	@docker-compose up --build -d
	# @docker exec -t airflow bash -c "airflow connections --add --conn_id oracle_destiny --conn_uri oracle://system:oracle@$(docker ps -aqf name=destination-db):49161/xe"

rebuild:
	@echo "Rebuilding CodeForces-ETL"
	@make clean
	@make build


start:
	@echo "Starting CodeForces-ETL"
	@docker-compose start

play:
	@echo "Starting CodeForces-ETL"
	@docker-compose start

stop:
	@echo "Stopping CodeForces-ETL"
	@docker-compose stop

clean:
	@echo "Cleaning CodeForces-ETL"
	@docker-compose down
	@docker volume rm airflow