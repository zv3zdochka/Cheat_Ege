FROM python:3.12
LABEL authors="batsi"
COPY ScrappedSearch.py .
COPY requirements.txt .
COPY data.json .
COPY log.txt .
COPY help.txt .
COPY found.txt .
COPY users.json .
RUN pip install -r requirements.txt
CMD ["python", "ScrappedSearch.py"]
