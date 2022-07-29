include .env
shell_name = zsh

# DEBUG==Trueのときはflaskを起動し、Falseのときはgunicornを起動する
ifeq ($(DEBUG),True)
	run_commnad = python app/app.py
else
	run_commnad = gunicorn --bind :$(PORT) --reload app.app:app
endif


# docker-build docker-server
all: server

## docker image関連
# dockerfile->imageの作成
.PHONY: build
build:
	docker build -t gcr.io/$(PROJECT_ID)/$(IMAGE_NAME) .

# GCRへのpush
.PHONY: push
push:
	docker push gcr.io/$(PROJECT_ID)/$(IMAGE_NAME)

## dockerの確認コマンド
# 確認
.PHONY: images
images:
	docker images

# コンテナを一覧表示
.PHONY: ps
ps:
	docker compose ps -a

# dockerのlogを表示
.PHONY: logs
logs:
	docker compose logs

## dockerの実行コマンド
.PHONY: up
up:
	docker compose up -d --build

# 実行
.PHONY: exec
exec:
	@make up
	docker compose exec app ${shell_name}

# serverを起動
.PHONY: server
server:
	@make up
	docker compose exec app ${run_commnad}

# serverをバックグラウンドで起動
.PHONY: server-production
server-production:
	@make up
	docker compose exec -d app ${run_commnad}

# コンテナを停止
.PHONY: stop
stop:
	docker compose stop

# コンテナを停止して削除
.PHONY: down
down:
	docker compose down --remove-orphans

# dockerの未使用オブジェクトを削除
.PHONY: prune
prune:
	docker system prune -af

## docker内で扱うコマンド
# serverを起動
.PHONY: server-in-docker
server-in-docker:
	cd app && ${run_commnad}

# pip freeze
.PHONY: pip-freeze
pip-freeze:
	docker compose exec app pip freeze > requirements.txt

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
