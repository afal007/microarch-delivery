.PHONY: install-rye install deps test

# Install Rye if not installed
install-rye:
	@source "$$HOME/.rye/env"; \
	if ! command -v rye &> /dev/null; then \
		echo "Rye not found. Installing..."; \
		curl -sSf https://rye.astral.sh/get | bash; \
		source "$$HOME/.rye/env"; \
	fi

# Ensure Rye is installed, then install dependencies
install: install-rye
	@source "$$HOME/.rye/env"; \
	rye sync;

# Install dependencies (shortcut)
deps: install

# Run tests
test: install
	@source "$$HOME/.rye/env"; \
	rye test;