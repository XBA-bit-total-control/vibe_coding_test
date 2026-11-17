FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /usr/local/bin/uv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src/ ./src/
RUN SECRET_KEY=collectstatic-build-only python src/manage.py collectstatic --noinput

USER 10001:10001
EXPOSE 8000

CMD ["sh", "-c", "python src/manage.py migrate --noinput && exec uvicorn todo_web_cite.asgi:application --app-dir src --host 0.0.0.0 --port 8000"]
