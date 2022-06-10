## dockerコマンド
# 確認
images:
	docker images
ps:
	docker ps -a
volume:
	docker volume ls
logs:
	docker compose logs

# 実行
build:
	docker compose build --no-cache --force-rm
up:
	docker compose up -d --build
.PHONY: app
app:
	docker compose exec app sh
root:
	docker compose exec -u root app sh
create-docker-project:
	docker build -t app .
	docker run -e PORT=8000 -p 8000:8000 --rm app
create-project:
	@make build
	@make up
	@make app
stop:
	docker compose stop
down:
	docker compose down --remove-orphans
restart:
	@make down
	@make up
	@make app
destroy:
	docker compose down --rmi all --volumes --remove-orphans
destroy-volumes:
	docker compose down --volumes --remove-orphans
prune:
	docker system prune
