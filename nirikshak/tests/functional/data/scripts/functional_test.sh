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

echo "Current working directoru $PWD"
cp /root/workers/process/inifinity.py /usr/local/bin/inifinity

inifinity &

echo "Running process ....."
ps -eaf

echo "Running deployment group ...."
nirikshak --groups=deployment
