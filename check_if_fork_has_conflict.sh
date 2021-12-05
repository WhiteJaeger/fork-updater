#!/bin/bash

# Arguments
## 1: tmp folder id
## 2: fork url
## 3: upstream url
## 4: user

TMP_FOLDER_ID="$1"
FORK_URL="$2"
UPSTREAM_URL="$3"
GH_USER="$4"

# Create dir for fork
mkdir -m 770 -p "/tmp/forkUpdate${TMP_FOLDER_ID}"
pushd "/tmp/forkUpdate${TMP_FOLDER_ID}"

# Need to remove 'https://'
FORK_URL="${FORK_URL:8}"
FORK_URL="https://x-access-token:${AUTH_TOKEN}@${FORK_URL}"

git clone "${FORK_URL}" fork

pushd fork

git pull

git config user.name "${GH_USER}"
git config user.email "${GH_USER}@users.noreply.github.com"

git remote add upstream "${UPSTREAM_URL}"

git remote update

# Check if the main branch of the fork has conflicts with the main branch of the upstream
git merge upstream/main --no-ff --no-commit
# 0 means that there is no conflict, 1 means that there is
MERGE_EXIT_CODE=$?

# Clean-up
pushd /tmp

rm -rf "/tmp/forkUpdate${TMP_FOLDER_ID}"

exit $MERGE_EXIT_CODE
