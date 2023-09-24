FROM python:3.9

COPY systemet.py / 

RUN pip install pytest-playwright && playwright install && playwright install-deps

CMD [ "python", "systemet.py" ]
