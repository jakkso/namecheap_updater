FROM python:3-onbuild
RUN pip install --upgrade pip
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .
COPY namecheap ./namecheap/.

ENTRYPOINT ["python", "run.py"]
