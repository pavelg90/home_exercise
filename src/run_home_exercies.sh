#!/bin/bash

# Define the repository details
REPO_URL="https://github.com/username/repo-name.git"
LOCAL_DIR="/path/to/local/directory"

# Clone the repository
git clone $REPO_URL $LOCAL_DIR

# Move into the directory
cd $LOCAL_DIR

# Build and run the containers in detached mode
docker-compose up --build -d
