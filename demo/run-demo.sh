#!/usr/bin/env bash

if ! (which cf.py > /dev/null 2>&1); then
	export PATH="$PATH:$(cd ..; pwd)"
	export PYTHONPATH="$PATH:$(cd ../lib; pwd)"
fi

rm -rf contest
cf.py init_folder contest
pushd contest
cf.py start A

popd

tree contest

