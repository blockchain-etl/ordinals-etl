FROM python:3.6-alpine
ENV PROJECT_DIR=ordinals-etl

RUN mkdir /$PROJECT_DIR
WORKDIR /$PROJECT_DIR
COPY . .

RUN pip install --upgrade pip && pip install -e /$PROJECT_DIR/

ENTRYPOINT ["python", "ordinalsetl"]