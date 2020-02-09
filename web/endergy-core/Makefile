docker-user=jaredhanson11
name=${docker-user}/endergy-core

build:
	docker build . -t ${name}:latest
push: build
	docker push ${name}:latest
