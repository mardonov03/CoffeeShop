celery -A internal.tasks.mail worker --loglevel=info --pool=solo
uvicorn app.main:app --reload --port 8081