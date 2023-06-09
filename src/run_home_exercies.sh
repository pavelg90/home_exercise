#!/bin/bash

# Define the repository details
REPO_URL="https://github.com/pavelg90/home_exercise.git"
LOCAL_DIR="C:\Users\User\Desktop\Projects\ireg\home_exercise_repo"

# Remove the existing directory if it exists
if [ -d "$LOCAL_DIR" ]; then
    rm -rf $LOCAL_DIR
fi

# Clone the repository
git clone $REPO_URL $LOCAL_DIR

# Move into the directory
cd $LOCAL_DIR

# Build and run the containers in detached mode
docker-compose up --build -d
