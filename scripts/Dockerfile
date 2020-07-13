FROM python:3.7.5-slim

ARG directory_path

COPY list_duplicates.py list_duplicates.py

RUN mkdir -p dup_dir

ADD ${directory_path} dup_dir

ENTRYPOINT ["python", "list_duplicates.py", "dup_dir"]
