app ?= whoami

app:
	docker-compose -f compose.yaml -f compose.$(app).yaml up --build --remove-orphans

clean:
	docker-compose down -v --remove-orphans
