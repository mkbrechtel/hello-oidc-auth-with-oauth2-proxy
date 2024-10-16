default: fastapi
always:

no-app:
	docker-compose -f compose.yaml up --remove-orphans

app:
	docker-compose -f compose.yaml -f compose.$(app).yaml up --build --remove-orphans

fastapi: always
	make app app=fastapi
