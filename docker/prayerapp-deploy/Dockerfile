FROM lambci/lambda:build-python3.6

# Install nodejs ( base image has node, but not npm? )
RUN \
  curl -sL https://rpm.nodesource.com/setup_9.x | bash && \
  yum install -y nodejs && \
  yum clean all

WORKDIR /app

# install npm modules
COPY ./package.json ./package-lock.json /app/
RUN npm install

# fetch py dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir \
  --requirement ./requirements.txt

# add app
COPY ./serverless.yml /app/
COPY ./dist /app/dist
RUN \
  pip install \
    --no-index \
    --find-links dist \
    --target . \
    prayerapp