FROM python:3.12
LABEL authors="batsi"
COPY Search.py .
COPY requirements.txt .
COPY data.json .
COPY log.txt .
COPY help.txt .
COPY found.txt .
COPY users.json .
RUN pip install -r requirements.txt
CMD ["python", "Search.py"]
