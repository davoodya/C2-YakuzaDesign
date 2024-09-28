#!/bin/bash

# List of users
users=("davoodya" "hossein" "korosh" "daria" "aria")

# Run the Python script for each user
for user in "${users[@]}"
do
    sudo -u "$user" python3 ./c2_client.py &
done

# Wait for all background processes to complete
# wait


