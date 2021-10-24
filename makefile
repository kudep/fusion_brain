SHELL:=/bin/bash
DOCKER_COMPOSE=docker-compose -f docker-compose.yml -f gpus.yml

.PHONY: install_env down_env build_env up_env up_build_env
.PHONY: run_test run_format run_agent

# run by default up_env
all: up_env
# install shortcuts
install_env:
	echo NETWORK_NAME=${PWD##*/}_agent_$(cat /dev/urandom | tr -dc '0-9' | fold -w 5 | head -n 1) > .env
	docker build -t prochtenie_service_test_creater:1.0 tests/service_test_creater/
	docker build -t prochtenie_linter:1.0 tests/linter/
	mkdir -p data/{deeppavlov,services,datasets,tfhub,saved_reports} pku
	mkdir -p pku
	bash tools/load_data.sh
	bash tools/init_gpus_file.sh
	bash tools/install_pku.sh

# docker shortcuts
down_env:
	${DOCKER_COMPOSE} down
build_env:
	${DOCKER_COMPOSE} build --no-cache
up_env:
	${DOCKER_COMPOSE} up -d
	bash tools/ping_services.sh
up_build_env:
	${DOCKER_COMPOSE} up -d --build
	bash tools/ping_services.sh
	docker-compose -f docker-compose.yml -f gpus.yml exec agent bash misc/enable_logging.sh

install_pku:
	bash tools/install_pku.sh

run_agent:
	bash tools/test_agent.sh

run_test:
	docker run --rm --user $(id -u):$(id -g) -v ${PWD}:/data prochtenie_linter:1.0 bash lint.sh
	bash tools/test_services.sh

run_format:
	docker run --rm --user $(id -u):$(id -g) -v ${PWD}:/data prochtenie_linter:1.0 bash format.sh

run_pku:
	bash tools/run_pku.sh

run_greedy_report:
	bash tools/make_greedy_report.sh

run_full_report:
	bash tools/make_full_report.sh

update_all_tests:
	bash tools/update_all_service_tests.sh
