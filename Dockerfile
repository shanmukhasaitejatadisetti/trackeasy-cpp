FROM python:3.12-slim
EXPOSE 8000
WORKDIR /opt/server
ENV PYTHONDONTWRITEBYTECODE 1 \
    && PYTHONUNBUFFERED 1
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "vehicle_order_management.wsgi:application", "--bind", "0.0.0.0:8000"]