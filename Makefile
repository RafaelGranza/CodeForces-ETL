all:
	@echo "Commands:\n"
	@echo "   Build the dockers:"
	@echo "      make build\n"
	@echo "   Start the dockers:"
	@echo "      make start\n"
	@echo "   Stop the dockers:"
	@echo "      make stop\n"
	@echo "   Clean the dockers:"
	@echo "      make clean\n"
	

build:
	@echo "Building CodeForces-ETL"
	@docker-compose up -d

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
