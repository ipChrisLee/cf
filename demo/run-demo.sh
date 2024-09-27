#!/usr/bin/env bash

if ! (which cf.py > /dev/null 2>&1); then
	export PATH="$PATH:$(cd ..; pwd)"
fi

cf.py init_folder contest
pushd contest
cf.py start A

popd

tree contest

