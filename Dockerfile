FROM continuumio/miniconda
WORKDIR  /opt/backend
RUN pwd
COPY . .
RUN conda env update -f environment.yml
WORKDIR  /opt/backend/adso_core
RUN pip install .
WORKDIR  /opt/backend 
EXPOSE 8000
# CMD ["./manage.py runserver 0:8000"]