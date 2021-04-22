#!/bin/bash

# install docker
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose -y
sudo apt-get install pass gnupg2 -y
getent group docker || sudo groupadd docker
sudo usermod -aG docker $USER

# python (pip3)
sudo apt-get install python3-pip -y

# AWS CLI
rm -rf "/home/$USER/aws"
sudo apt-get install unzip -y
AWSCLI_PATH="/home/$USER/awscliv2.zip"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o $AWSCLI_PATH
(cd "/home/$USER" && unzip awscliv2.zip && sudo ./aws/install)

# Mysql client
sudo apt install mysql-client-core-5.7 -y

echo ""
echo "---------------------------------------------"
echo "Versions:"
echo "---------------------------------------------"

printf "\e[93m"

docker --version
docker-compose --version
python3 --version
aws --version

printf "\e[0m"

# re-login
echo ""
printf "\e[32mThe preparation has been completed successfully!\e[0m\n"
echo ""
printf "\e[32mAuto logout!\e[0m\n"
echo ""
kill -SIGHUP $PPID