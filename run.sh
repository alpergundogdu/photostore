poetry run uvicorn photostore.app:app --env-file local.config --port ${1:-8000}

