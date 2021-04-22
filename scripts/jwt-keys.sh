#!/bin/sh

jwtsecret="jwt.pem"
jwtpublic="jwt.pub"

if [ "$1" != "" ]; then
    DIR=$1
else
    #DIR="$(dirname "$(readlink -f "$0")")"
    DIR="users"
fi

if [ ! -e "$DIR/$jwtsecret" ]; then
       openssl ecparam -genkey -name secp521r1 -noout -out "$DIR/$jwtsecret"
       openssl ec -in "$DIR/$jwtsecret" -pubout -out "$DIR/$jwtpublic"
fi