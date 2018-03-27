#/bin/bash

echo "Creating temporary director ...."
mkdir -p func-tests-build/logs

FUNCTIONAL_TEST_DIR=nirikshak/tests/functional/data
FUNCTIONAL_TEST_CASE_STATUS=true

echo "Clean output file ...."
rm $PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.json

echo "Running Test cases for result.json .."
docker run -it --rm \
              --hostname functional \
              --name functional \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/etc/nirikshak/nirikshak.conf",target="/etc/nirikshak/nirikshak.conf" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak",target="/var/lib/nirikshak" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/scripts/functional_test.sh",target="/home/functional_test.sh" \
              --mount type=bind,src="$PWD/func-tests-build/logs/nirikshak.log",target="/var/log/nirikshak.log" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/workers/",target="/root/workers/" \
              --mount type=bind,src="$PWD",target="/nirikshak" \
              thenakliman/nirikshak_functional_test:latest

diff $PWD/$FUNCTIONAL_TEST_DIR/expected_outputs/result.json $PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.json

if [ $? -eq 0 ]; then
    echo "Result.json passed"
else
    echo "result.json failed"
    FUNCTIONAL_TEST_CASE_STATUS=false
fi

if [ "$dev_env" = false ]; then
    echo "Clean output file ...."
    rm $PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.json
fi

if [ "$FUNCTIONAL_TEST_CASE_STATUS" == false ]; then
    exit 1
fi
