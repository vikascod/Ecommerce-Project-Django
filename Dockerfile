FROM Python:3.10.10

ENV PYTHONBUFFERED=1

WORKDIR /Bloommerce

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver" ]