#!/usr/bin/env bash

if ! (which cf.py > /dev/null 2>&1); then
	export PATH="$PATH:$(cd ..; pwd)"
	export PYTHONPATH="$PATH:$(cd ../lib; pwd)"
fi

rm -rf contest

cf.py init_folder contest
pushd contest
cf.py start A --lang cpp --t_limit 2
cf.py build A
cf.py start B --lang py
cf.py start C --lang cpp --t_limit 3
cf.py run C

popd

tree contest

