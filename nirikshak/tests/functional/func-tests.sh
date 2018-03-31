#/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "Creating temporary director ...."
mkdir -p func-tests-build/logs

FUNCTIONAL_TEST_DIR=nirikshak/tests/functional/data
FUNCTIONAL_TEST_CASE_STATUS=true

cleanup_output_file() {
    rm $1
}

compare_against_expected_output() {
    diff $1 $2
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}****************** PASSED *****************${NC}"
    else
        echo -e "${RED}****************** FAILED *****************${NC}"
        FUNCTIONAL_TEST_CASE_STATUS=false
    fi
}

run_test() {
    OUTPUT_FILE=$2
    EXPECTED_OUTPUT_FILE=$1
    GROUPS_TO_RUN=$3
    echo "Clean output file"
    cleanup_output_file $OUTPUT_FILE

    docker run -it --rm \
              --hostname functional \
              --name functional \
              --env GROUPS=$GROUPS_TO_RUN \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/etc/nirikshak/nirikshak.conf",target="/etc/nirikshak/nirikshak.conf" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak",target="/var/lib/nirikshak" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/scripts/functional_test.sh",target="/home/functional_test.sh" \
              --mount type=bind,src="$PWD/func-tests-build/logs/nirikshak.log",target="/var/log/nirikshak.log" \
              --mount type=bind,src="$PWD/$FUNCTIONAL_TEST_DIR/workers/",target="/root/workers/" \
              --mount type=bind,src="$PWD",target="/nirikshak" \
              thenakliman/nirikshak_functional_test:latest

    compare_against_expected_output $OUTPUT_FILE $EXPECTED_OUTPUT_FILE
    if [ "$dev_env" = false ]; then
        echo "Clean output file ...."
        rm $OUTPUT_FILE
    fi
}

echo "Running Test cases for JSON Output .."
run_test "$PWD/$FUNCTIONAL_TEST_DIR/expected_outputs/result.json" "$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.json" "deployment"
run_test $PWD/$FUNCTIONAL_TEST_DIR/expected_outputs/result.yaml "$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.yaml" "monitor"
run_test $PWD/$FUNCTIONAL_TEST_DIR/expected_outputs/result.csv "$PWD/$FUNCTIONAL_TEST_DIR/var/nirikshak/result.csv" "pipeline"

if [ "$FUNCTIONAL_TEST_CASE_STATUS" == false ]; then
    exit 1
fi
