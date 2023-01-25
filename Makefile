build-api:
	docker-compose build api

build-ui: install-ui
	npm run build --prefix jaanevis/ui

install-ui:
	npm install --prefix jaanevis/ui
