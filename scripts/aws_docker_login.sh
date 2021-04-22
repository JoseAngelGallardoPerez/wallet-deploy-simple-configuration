#!/bin/sh

# Local .env
if [ -f .env ]; then
    # Load Environment Variables
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

aws --version | grep -Eq '(aws-cli\/2.*)$'
if [ $? -ne 0 ]; then
  printf "\e[31mPlease install \e[93maws-cli v2\e[31m!\e[0m\n"
  exit 1
fi

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"