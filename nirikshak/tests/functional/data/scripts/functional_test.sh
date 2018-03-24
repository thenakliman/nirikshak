echo "Cloning repository"
git clone https://github.com/thenakliman/nirikshak

echo "Chaing directory ..."
cd /nirikshak

echo "Installing latest code of nirikshak..."
python setup.py install

echo "Current working directoru $PWD"
python /root/workers/process/inifinity.py &

echo "Running deployment group ...."
nirikshak --groups=deployment
