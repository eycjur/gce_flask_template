include .env
shell_name = zsh

# docker-build docker-server
all: docker-build docker-server

## docker関連
# dockerfile->imageの作成
.PHONY: docker-build
docker-build:
	docker build -t $(CONTAINER_NAME) .
	docker tag $(CONTAINER_NAME) gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

# GCRへのpush
.PHONY: docker-push
docker-push:
	docker push gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

# GCRからのpull
.PHONY: docker-pull
docker-pull:
	docker pull gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME)

# docker runして接続
.PHONY: docker-run
docker-run:
	docker run \
	--rm \
	-it \
	-v $(shell pwd)/app:/app \
	-p $(PORT):$(PORT) \
	--env-file $(shell pwd)/.env \
	gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
	${shell_name}

# serverを起動
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

# serverをバックグラウンドで起動
.PHONY: docker-server-production
docker-server-production:
	docker run \
	--rm \
	-d \
	-v $(shell pwd)/app:/app \
	-p $(PORT):$(PORT) \
	--env-file $(shell pwd)/.env \
	gcr.io/$(PROJECT_ID)/$(CONTAINER_NAME) \
	gunicorn --bind :$(PORT) --reload app:app

# dockerのlogを表示
.PHONY: logs
logs:
	docker logs $(shell docker ps --quiet | head -n 1)

# dockerのcontainerを停止
.PHONY: stop
stop:
	docker stop $(shell docker ps --quiet | head -n 1)

# dockerの未使用オブジェクトを削除
.PHONY: prune
prune:
	docker system prune -af

## docker内で扱うコマンド
# serverを起動
.PHONY: server
server:
	cd app && gunicorn --bind :${PORT} --reload app:app

## GCP関連
# startup-scriptを実行
.PHONY: startup
startup:
	sudo google_metadata_script_runner startup

# startup-scriptのログを表示
.PHONY: startup-log
startup-log:
	sudo journalctl -u google-startup-scripts.service

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | python3 -u -c 'import sys, re; rx = re.compile(r"^[a-zA-Z0-9\-_]+:"); lines = [line.rstrip() for line in sys.stdin if not line.startswith(".PHONY")]; [print(f"""{line.split(":")[0]:20s}\t{prev.lstrip("# ")}""") if rx.search(line) and prev.startswith("# ") else print(f"""\n\033[92m{prev.lstrip("## ")}\033[0m""") if prev.startswith("## ") else "" for prev, line in zip([""] + lines, lines)]'
