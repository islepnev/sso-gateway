# Define reusable variables
CONFIG_DIR = config
TEST_CONFIG_DIR = docker/sso-gateway/config
EXAMPLE_CONFIG_DIR = docs
DOCKER_COMPOSE = docker/docker-compose.yml
DEV_CONTAINERS = apache-proxy sso-gateway dummy-api
PYTHON = python
SSO_GATEWAY_MODULE = app.main
DEVEL_REQUIREMENTS = requirements-devel.txt

# Help target to list available commands
.PHONY: help
help: ## List all available makefile targets
	@echo "Available makefile targets:"
	@awk '/^[a-zA-Z0-9_-]+:.*?## / { printf "\033[36m%-25s\033[0m %s\n", $$1, substr($$0, index($$0, "## ") + 3) }' $(MAKEFILE_LIST)

# Build development Docker images
.PHONY: build
build: ## Build development Docker images
	@docker-compose -f $(DOCKER_COMPOSE) build

# Run unit tests
.PHONY: test
test: install-dev ## Run unit tests (installs development dependencies if needed)
	@$(PYTHON) -m unittest discover tests

# Run sso-gateway app locally
.PHONY: run-local
run-local: ## Run sso-gateway app locally with live reload
	@$(PYTHON) -m uvicorn $(SSO_GATEWAY_MODULE):app --reload --host 127.0.0.1 --port 8000

# Run sso-gateway app in a container
.PHONY: run-container
run-container: ## Run sso-gateway app in a container
	@docker-compose -f $(DOCKER_COMPOSE) up sso-gateway

# Start all development containers
.PHONY: up
up: ## Start all development containers
	@docker-compose -f $(DOCKER_COMPOSE) up -d $(DEV_CONTAINERS)

# Stop all development containers
.PHONY: down
down: ## Stop all development containers
	@docker-compose -f $(DOCKER_COMPOSE) down

# Clean development containers and images
.PHONY: clean
clean: ## Clean up development containers and images
	@docker-compose -f $(DOCKER_COMPOSE) down --rmi local --volumes --remove-orphans

# Initialize config for local development
.PHONY: init-config
init-config: ## Initialize local development config
	@mkdir -p $(CONFIG_DIR)
	@echo "Initializing local config in $(CONFIG_DIR)..."
	@cp -n $(EXAMPLE_CONFIG_DIR)/config_example.yaml $(CONFIG_DIR)/config.yaml || echo "$(CONFIG_DIR)/config.yaml already exists"
	@cp -n $(EXAMPLE_CONFIG_DIR)/secrets_example.yaml $(CONFIG_DIR)/secrets.yaml || echo "$(CONFIG_DIR)/secrets.yaml already exists"

# Initialize config for integration test
.PHONY: init-config-test
init-config-test: ## Initialize integration test config
	@mkdir -p $(TEST_CONFIG_DIR)
	@echo "Initializing integration test config in $(TEST_CONFIG_DIR)..."
	@cp -n $(EXAMPLE_CONFIG_DIR)/config_example.yaml $(TEST_CONFIG_DIR)/config.yaml || echo "$(TEST_CONFIG_DIR)/config.yaml already exists"
	@cp -n $(EXAMPLE_CONFIG_DIR)/secrets_example.yaml $(TEST_CONFIG_DIR)/secrets.yaml || echo "$(TEST_CONFIG_DIR)/secrets.yaml already exists"

# Install development dependencies
.PHONY: install-dev
install-dev: ## Install development and testing dependencies
	@if [ -f $(DEVEL_REQUIREMENTS) ]; then \
		$(PYTHON) -m pip install -r $(DEVEL_REQUIREMENTS); \
	else \
		echo "$(DEVEL_REQUIREMENTS) not found. Skipping development dependency installation."; \
	fi
