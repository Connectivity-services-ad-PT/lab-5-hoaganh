.PHONY: compose-up compose-down logs test-compose

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

logs:
	docker compose logs -f

test-compose:
	npx newman run postman/collections/FIT4110_lab05_core.postman_collection.json \
		-e postman/environments/FIT4110_lab05_local.postman_environment.json \
		-r cli,junit,htmlextra \
		--reporter-junit-export reports/newman-lab05-compose.xml \
		--reporter-htmlextra-export reports/newman-lab05-compose.html
