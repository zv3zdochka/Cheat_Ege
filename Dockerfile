FROM python:latest
LABEL authors="batsi"
COPY Search.py .
COPY requirements.txt .
COPY data.json .
RUN pip install -r requirements.txt
CMD ["python", "Search.py", "data.json", "2"]
