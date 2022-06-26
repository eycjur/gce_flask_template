include .env

all: docker-build docker-server

# docker関連
.PHONY: docker-build
docker-build:
	docker build -t $(CONTAINER_NAME) .
	docker tag $(CONTAINER_NAME) gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

.PHONY: docker-push
docker-push:
	docker push gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

.PHONY: docker-pull
docker-pull:
	docker pull gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

.PHONY: docker-run
docker-run:
	docker run \
	--rm \
	-it \
	-v $(shell pwd)/app:/app \
	-p $(PORT):$(PORT) \
	--env-file $(shell pwd)/.env \
	gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
	bash

.PHONY: docker-server
docker-server:
	docker run \
	--rm \
	-it \
	-v $(shell pwd)/app:/app \
	-p $(PORT):$(PORT) \
	--env-file $(shell pwd)/.env \
	gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
	gunicorn --bind :$(PORT) --reload app:app

.PHONY: server
server:
	cd app && gunicorn --bind :${PORT} --reload app:app
