#!/bin/bash

set -e

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

# Update based on the strategy
## getNew: just get new changes from the upstream
## keepFork: resolve conflicts in favour of the fork, keep the original state, get new changes
## keepUpstream: resolve conflicts in favour of the upstream, rewrite the original state, get new changes

# TODO: pass as arg?
LABS_TO_UPDATE=(1 2)

if [[ "$STRATEGY" == "getNew" ]]; then
  # Just get new changes
  git merge --no-edit upstream/main
elif [[ "$STRATEGY" == "keepFork" ]]; then
  # Merge in favour of the forked repository
  git merge --strategy-option ours --no-edit upstream/main

  for lab in "${LABS_TO_UPDATE[@]}"; do

    git checkout origin/main -- lab_"${lab}"/start.py
    git checkout origin/main -- lab_"${lab}"/main.py

  done

  git commit -m "get latest changes from the original repository" || true

elif [[ "$STRATEGY" == "keepUpstream" ]]; then
  # Merge in favour of the upstream repository
  git merge --strategy-option theirs --no-edit upstream/main

  for lab in "${LABS_TO_UPDATE[@]}"; do

    git checkout upstream/main -- lab_"${lab}"/start.py
    git checkout upstream/main -- lab_"${lab}"/main.py

  done

  git commit -m "get latest changes from the original repository" || true

fi

git push origin HEAD:main

pushd /tmp

rm -rf "/tmp/forkUpdate${TMP_FOLDER_ID}"
