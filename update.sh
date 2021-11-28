#!/bin/bash

# Arguments
## 1: tmp folder id
## 2: fork url
## 3: upstream url
## 4: user
## 5: update strategy

TMP_FOLDER_ID="$1"
FORK_URL="$2"
UPSTREAM_URL="$3"
GH_USER="$4"
STRATEGY="$5"

echo "$STRATEGY"

# Create dir for fork
mkdir -m 770 -p "/tmp/forkUpdate${TMP_FOLDER_ID}"
pushd "/tmp/forkUpdate${TMP_FOLDER_ID}"

# Need to remove 'https://'
FORK_URL="${FORK_URL:8}"
FORK_URL="https://x-access-token:${AUTH_TOKEN}@${FORK_URL}"

echo "$FORK_URL"

git clone "${FORK_URL}" fork

pushd fork

git pull

git config user.name "${GH_USER}"
git config user.email "${GH_USER}@users.noreply.github.com"

git remote add upstream "${UPSTREAM_URL}"

git remote -v

git remote update

git merge --no-edit upstream/main

git push origin HEAD:main

pushd /tmp

rm -rf "/tmp/forkUpdate${TMP_FOLDER_ID}"
