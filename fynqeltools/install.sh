#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "Installing fynqeltools..."

BASE_DIR="/data/data/com.termux/files/usr/share/fynqeltools"
HOME_DIR="$BASE_DIR/home/file"

mkdir -p "$HOME_DIR"

cp fynq.py "$PREFIX/bin/fynq"
chmod +x "$PREFIX/bin/fynq"

echo "fynqeltools installed successfully"
