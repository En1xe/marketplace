FROM python:3.14-alpine

RUN pip install uv

WORKDIR /app/

COPY ./pyproject.toml ./uv.lock* ./

RUN uv pip install --system .

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]