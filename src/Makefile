run:
	uvicorn main:app --reload

celery:
	celery -A core.celery.celery_app worker --loglevel=info

beat:
	celery -A core.celery.celery_app beat --loglevel=info

start:
	make celery & make beat
