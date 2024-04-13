FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r ./project/requirements.txt

EXPOSE 3000

# run in development mode
ENV FLASK_ENV=development

# "--host=0.0.0.0" is a built-in development server
CMD "python app.py"
