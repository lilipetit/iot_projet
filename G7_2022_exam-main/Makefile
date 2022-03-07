db-migrate:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1
run:
	cd app && uvicorn main:app --host=0.0.0.0 --port=8000 --reload