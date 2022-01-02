TAG = latest
APP = $(shell basename $(CURDIR))
build:
	docker build -t $(APP):$(TAG) .

run:
	docker run  --rm -e FLASK_ENV=development -p 5000:5000 -it $(APP):$(TAG)

test:
	docker run  --rm -e FLASK_ENV=development -it $(APP):$(TAG) pytest --cov --cov-report=term --cov=report=xml

lint:
	docker run  --rm -e FLASK_ENV=development -it $(APP):$(TAG) flake8
