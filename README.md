[![Build Status](https://travis-ci.org/mottaquikarim/PrayerApp.svg?branch=master)](https://travis-ci.org/mottaquikarim/PrayerApp) [![Test Coverage](https://api.codeclimate.com/v1/badges/3797d09b2aee38a8b56e/test_coverage)](https://codeclimate.com/github/mottaquikarim/PrayerApp/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/3797d09b2aee38a8b56e/maintainability)](https://codeclimate.com/github/mottaquikarim/PrayerApp/maintainability)

# PrayerApp

*🎉🎈🎂🍾🎊🍻💃*

*Simple app that returns times to pray based on lat, lon, and timestamp.*

**NOTE**: This is currently a work in progress, porting over implementation from a private repo.

## Usage and Installation

From terminal, pull down this repo:

```
$ git clone https://github.com/mottaquikarim/PrayerApp
```

Then, assert that:

```
$ docker -v
# Docker version 17.12.0-ce (or greater)
$ docker-compose -v
# docker-compose version 1.18.0
```

(**NOTE**: app requires docker-compose version 2.1 or greater, main reason for checking this)

Finally:

```
$ make test
```

Will build app and run tests. 

For a _quick and dirty_ test run that won't build docker every time:

```
$ virtualenv -p python3 .venv
```

(**NOTE**: you need to create virtualenv only **once**). After creation:

```
$ make quick-test
```

This will activate `.venv`, run tests, deactivate. **NOTE**: currently `make quick-test` is failing.


## Features

## To Dos
