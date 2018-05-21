#!/bin/bash

set -exo pipefail

pytest ./test
EXIT_CODE=$?

exit ${EXIT_CODE}
