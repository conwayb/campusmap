package = campusmap

init: docker-externals
	docker-compose build

reinit: docker-externals
	docker-compose build --no-cache

run:
	docker-compose up

docker-externals:
	docker network create --driver bridge $(package) || true
	docker volume create $(package)-geoserver-data
	docker volume create $(package)-postgres-data

.PHONY = init reinit run docker-externals
