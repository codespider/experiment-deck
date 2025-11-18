# experiment-deck

A Python experiment playground.

## Setup

```bash
# Install dependencies
uv sync

# Start Redis & PostgreSQL services
docker compose up -d
```

## Run

```bash
uv run main.py
```

## Using Just (alternative)

You can also use the Justfile for common commands:

```bash
just up    # Start services
just down  # Stop services
just run   # Run the app
just       # List all commands
```
