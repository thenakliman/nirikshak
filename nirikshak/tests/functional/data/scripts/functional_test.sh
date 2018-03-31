#if [ "$dev_env" = true ]; then
#    echo "Cloning repository"
#    git clone https://github.com/thenakliman/nirikshak
#fi

echo "Chaing directory ..."
cd /nirikshak

#if [ -z "$branch" ] && [ "${branch+xxx}" = "xxx" ]; then
#    echo "Checkout ci branch"
#    git checkout -b $branch
#fi

echo "Current branch "
git branch

echo "Installing latest code of nirikshak..."
python setup.py install

echo "Running socker listening server"
python "./nirikshak/tests/functional/data/output/send/listening_server.py" "./nirikshak/tests/functional/data/var/nirikshak/result.txt" 12345 &

echo "Current working directoru $PWD"
cp /root/workers/process/inifinity.py /usr/local/bin/inifinity

inifinity &

echo "Running process ....."
ps -eaf

echo "Environment variables ..."
export

echo "Running $GROUPS group ...."
nirikshak --groups="$GROUPS"
