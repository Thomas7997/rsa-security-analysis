#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [paramètre1] [paramètre2] ..."
    exit 1
fi

for param in "$@"; do
	echo $param
    openssl rsa -noout -text -in $param
done