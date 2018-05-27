[![Build Status](https://travis-ci.org/mottaquikarim/PrayerApp.svg?branch=master)](https://travis-ci.org/mottaquikarim/PrayerApp) [![Test Coverage](https://api.codeclimate.com/v1/badges/3797d09b2aee38a8b56e/test_coverage)](https://codeclimate.com/github/mottaquikarim/PrayerApp/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/3797d09b2aee38a8b56e/maintainability)](https://codeclimate.com/github/mottaquikarim/PrayerApp/maintainability)

# PrayerApp

*🎉🎈🎂🍾🎊🍻💃*

*Simple app that returns times to pray based on lat, lon, and timestamp.*

This app exposes a simple web API for querying prayer times (in the islamic tradition) by space and time. See an example of the deployed app **[here](https://8ldbpgh8mh.execute-api.us-east-1.amazonaws.com/prod/location/40.7128/-74.0059)** (<strong><a href="https://mottaquikarim.github.io/PrayerApp/docs/index.html" target="_blank">Docs here</a></strong>). This app leverages the **[praytimes.org](http://praytimes.org/manual)** project to cacluate prayer times. It is worth noting that the version of the **praytimes.org** library used here requires a patch due to a python scope issue (not sure how to push that patch back upstream, the project seems largely abandoned).

This app is built and tested with Python3.6 and deployed to AWS Lambda using the Serverless Framework through Travis CI. We 
use Codeclimate to keep track of maintainability and test coverage.

There are currently no limitations on API usage on the `/prod` endpoint, which is CORS enabled (therefore, possible to use with frontend javascript). This policy will remain if and until there is a good reason to restrict usage.

## Table of Contents
* <strong><a href="https://mottaquikarim.github.io/PrayerApp/docs/index.html" target="_blank">API Docs</a></strong>
* **[System Requirements](#system-requirements)**
* **[Usage and Installation](#usage-and-installation)**
* **[Secrets](#secrets)**
* **[Deployment](#deployment)**
* **[Todos](#todos)**
* **[Clients](#clients)**

### System Requirements

Here are the main tools and runtimes that I used to develop this project locally

```
$ docker -v # Docker version 17.12.0-ce (or greater)

$ docker-compose -v # docker-compose version 1.18.0

$ node -v # v8.1.2, or latest

$ python3 --version # Python 3.6.5, or Py3+
```

### Usage and Installation

From terminal, pull down this repo:

```
$ git clone https://github.com/mottaquikarim/PrayerApp
```

Then, assuming docker is running:

```
$ make test
```

Will build app and run tests. 

### Secrets

Secrets are managed through environment variables, fed in via CI (Travis) or manually exported in local environment. To run deployment and/or ftest in local environment, first export all env variables as defined in `envvars.sample`. **NOTE**: the app's Dockerfiles copy `envvars.sample` to `envvars`, which is used for container builds. 

#### Managing Travis Secrets
In order to run deployment process "for reals" (ie, to deploy to a prod env), the following env variables must be set (securely) in Travis settings:

* **`AWS_ACCESS_KEY_ID`**
* **`AWS_SECRET_ACCESS_KEY`**
* **`CC_TEST_REPORTER_ID`**
* **`GOOGLE_API_KEY`**

The **`CC_TEST_REPORTER_ID`** env variable is for code climate test coverage.


### Deployment

Serverless Framework is used to handle deployment. Look at [Serverless](https://serverless.com/framework/docs/getting-started/) getting started guide. 

Assuming `~/.aws/credentials` are exported to your envirnonment, simply run:

```
$ make clean deploy stage=test
```

Note that `stage` is a concept from AWS Lambda, it can be any arbitrary value (which will be reflected in the deployed lambda url, it is used mainly to segment environments).

If you don't have `~/.aws/credentials` folder or are not sure why it is needed, please take a look at [these docs](https://serverless.com/framework/docs/providers/aws/cli-reference/).

### Functional Tests

**[Robot Framework](http://robotframework.org/)** is used to handle functional tests. To run ftests (assuming deployment credentials are sorted out),

```
$ make clean deploy ftest stage=test
```

(Again, worth noting that envvars must be exported in order for ftests to pass)

### ToDos

* Get `/city/{city}/{country}` support back up
* Implement endpoint for IFTTT

### Clients

* [Ramadan2018](https://github.com/mottaquikarim/Ramadan2018)

*If you build a client that consumes this API, please submit a PR so we can showcase it here!*
