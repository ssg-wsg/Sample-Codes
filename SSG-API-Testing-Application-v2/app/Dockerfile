FROM python:3.12
WORKDIR /app
EXPOSE 80

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "Home.py"]
