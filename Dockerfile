FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

EXPOSE 8089

CMD ["uv", "run", "main.py"]