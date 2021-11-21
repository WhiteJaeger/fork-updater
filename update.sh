#!/bin/bash

mkdir -m 777 -p /tmp/forkUpdate

pushd /tmp/forkUpdate

FORK_URL="$1"
UPSTREAM_URL="$2"

git clone "git@github.com:WhiteJaeger/mock-2021.git" fork

pushd fork

git remote add upstream "${UPSTREAM_URL}"

git remote -v

git remote update

git merge --no-edit upstream/main

git push origin HEAD:main

pushd /tmp

rm -rf /tmp/forkUpdate
