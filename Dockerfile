FROM python:3.10.6-slim-bullseye as production
WORKDIR /workspace
COPY ./Pipfile ./Pipfile.lock /workspace/
RUN pip --no-cache-dir install pipenv \
 && pipenv install --deploy --system \
 && pip uninstall -y pipenv virtualenv-clone virtualenv
COPY . /workspace
ENTRYPOINT [ "pyvelocity" ]

FROM production as development
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip --no-cache-dir install pipenv \
 && pipenv install --deploy --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
