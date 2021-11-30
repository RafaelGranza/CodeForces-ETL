all:
	@echo "Commands:\n"
	@echo "   Build the dockers:"
	@echo "      make build\n"
	@echo "   Stop the dockers:"
	@echo "      make stop\n"
	@echo "   Clean the dockers:"
	@echo "      make clean\n"
	

build:
	@echo "Building CodeForces-ETL Airflow and OracleDB"
	@docker-compose up -d

stop:
	@echo "Stopping Airflow Docker"
	@docker-compose down

clean:
	@make stop
