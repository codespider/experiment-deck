default:
    @just --list

up:
    docker compose up -d

down:
    docker compose down

run:
    uv run main.py
