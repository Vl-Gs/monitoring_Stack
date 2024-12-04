.PHONY: install deploy test lint clean help

INVENTORY ?= inventories/production/hosts
PLAYBOOK ?= playbooks/main.yml
TAGS ?= all
LIMIT ?= all
VERBOSITY ?= 1

help:
	@echo "Available commands:"
	@echo "  make install    - Install Ansible requirements"
	@echo "  make deploy     - Deploy the monitoring stack"
	@echo "  make test       - Run Ansible syntax check"
	@echo "  make lint       - Run Ansible linting"
	@echo "  make clean      - Clean temporary files"
	@echo ""
	@echo "Variables:"
	@echo "  INVENTORY  - Path to inventory file (default: inventories/production/hosts)"
	@echo "  PLAYBOOK   - Path to playbook file (default: playbooks/main.yml)"
	@echo "  TAGS       - Ansible tags to run (default: all)"
	@echo "  LIMIT      - Limit to specific hosts (default: all)"
	@echo "  VERBOSITY  - Ansible output verbosity (default: 1)"

install:
	@echo "Installing Ansible requirements..."
	ansible-galaxy install -r requirements.yml

deploy:
	@echo "Deploying monitoring stack..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK) \
		--tags=$(TAGS) \
		--limit=$(LIMIT) \
		-$(VERBOSITY)

test:
	@echo "Running Ansible syntax check..."
	ansible-playbook -i $(INVENTORY) $(PLAYBOOK) --syntax-check

lint:
	@echo "Running Ansible linting..."
	ansible-lint $(PLAYBOOK)

clean:
	@echo "Cleaning temporary files..."
	find . -name "*.retry" -delete
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
