FROM python:3-alpine

WORKDIR /nperf

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY LICENSE .
COPY README.md .

COPY nperf.py .

CMD ["python","-u","nperf.py"]
