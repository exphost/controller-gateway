TAG = latest
APP = $(shell basename $(CURDIR))
build:
	docker build -t $(APP):$(TAG) .

run:
	docker run  --rm -e FLASK_ENV=development -e USERSSERVICE_ENDPOINT=http://127.0.0.0.1:8000 -e APPSSERVICE_ENDPOINT=http://localhost:8000 -e AUTH_ENDPOINT=https://auth.dev.exphost.pl/dex -p 5000:5000 -it $(APP):$(TAG)

test:
	docker run  --rm -e FLASK_ENV=development -it $(APP):$(TAG) pytest --cov --cov-report=term --cov=report=xml

lint:
	docker run  --rm -e FLASK_ENV=development -it $(APP):$(TAG) flake8
