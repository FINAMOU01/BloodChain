#!/bin/bash

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing base packages..."
sudo apt install -y curl git

echo "Basic VPS setup complete."