FROM python:3.7

COPY docker/prayerapp/test.sh /test.sh

# Install dependencies directly instead of through serverless plugin for development
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir \
  --requirement /tmp/requirements.txt

# Install prayerapp
COPY ./dist /tmp/dist
RUN \
  pip install \
  --no-index \
  --find-links /tmp/dist \
  prayerapp 

