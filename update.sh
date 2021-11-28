#!/bin/bash

# Arguments
## 1: tmp folder id
## 2: fork name
## 3: fork url
## 4: upstream url
## 5: user

TMP_FOLDER_ID="$1"
FORK_NAME="$2"
FORK_URL="$3"
UPSTREAM_URL="$4"
GH_USER="$5"

# Create dir for fork
mkdir -m 770 -p "/tmp/forkUpdate${TMP_FOLDER_ID}"
pushd "/tmp/forkUpdate${TMP_FOLDER_ID}"

# Need to remove 'https://'
FORK_URL="${FORK_URL:8}"
FORK_URL="https://x-access-token:${AUTH_TOKEN}@${FORK_URL}"

git config --global user.name "${USER}"
git config --global user.email "${USER}@users.noreply.github.com"

git clone "git@github.com:WhiteJaeger/mock-2021.git" fork

pushd fork

git remote add upstream "${UPSTREAM_URL}"

git remote -v

git remote update

git merge --no-edit upstream/main

git push origin HEAD:main

pushd /tmp

rm -rf /tmp/forkUpdate
