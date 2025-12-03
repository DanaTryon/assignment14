dev:
    @export DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db && \
    alembic upgrade head && \
    uvicorn app.main:app --reload

test:
    @export DATABASE_URL=postgresql://user:password@localhost:5432/mytestdb && \
    alembic upgrade head && \
    pytest
