FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "stocks_products.wsgi:application"]
