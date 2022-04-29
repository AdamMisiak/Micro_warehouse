# these will speed up builds, for docker-compose >= 1.25
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

build:
	docker-compose build

up:
	docker-compose up

up-daemon:
	docker-compose up -d

down:
	docker-compose down

test: up-daemon
	docker-compose run --rm --no-deps --entrypoint=pytest warehouse