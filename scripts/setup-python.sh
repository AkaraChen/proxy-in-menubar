#!/bin/bash

# Exit on error
set -e

PYTHON_VERSION="3.10.13"
RELEASE_TAG="20240107"
ARCH="aarch64-apple-darwin"
FILENAME="cpython-${PYTHON_VERSION}+${RELEASE_TAG}-${ARCH}-install_only.tar.gz"
URL="https://github.com/indygreg/python-build-standalone/releases/download/${RELEASE_TAG}/${FILENAME}"

RESOURCES_DIR="src-tauri/resources"
PYTHON_TARGET_DIR="${RESOURCES_DIR}/python"

echo "Setting up Python in ${PYTHON_TARGET_DIR}..."

mkdir -p "${RESOURCES_DIR}"

if [ -d "${PYTHON_TARGET_DIR}" ]; then
    echo "Python directory already exists, skipping download."
else
    echo "Downloading portable Python from ${URL}..."
    curl -L "${URL}" -o "python_standalone.tar.gz"
    
    echo "Extracting..."
    mkdir -p "${PYTHON_TARGET_DIR}"
    tar -xzf "python_standalone.tar.gz" -C "${PYTHON_TARGET_DIR}" --strip-components=1
    
    echo "Cleaning up..."
    rm "python_standalone.tar.gz"
fi

echo "Python setup complete."
