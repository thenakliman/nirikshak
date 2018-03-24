#/bin/bash

echo "Creating temporary director ...."
mkdir -p func-tests-build/logs

FUNCTIONAL_TEST_DIR=nirikshak/tests/functional/data

echo "Running Test cases for result.json .."
docker run -it --rm \
              --hostname functional \
              --name functional \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/etc/nirikshak/nirikshak.conf",target="/etc/nirikshak/nirikshak.conf" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak",target="/var/lib/nirikshak" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/scripts/functional_test.sh",target="/home/functional_test.sh" \
              --mount type=bind,src="$PWD/func-tests-build/logs/nirikshak.log",target="/var/log/nirikshak.log" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/workers/",target="/root/workers/" \
              thenakliman/nirikshak_functional_test:latest
