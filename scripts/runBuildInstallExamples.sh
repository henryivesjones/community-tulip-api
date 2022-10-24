#!/bin/bash
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

cd ..
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r dev-requirements.txt >/dev/null
echo "Installed DEV-REQUIREMENTS..."

rm -rf -f dist

python3 -m build >/dev/null
echo "Built community-tulip-api package."

cd dist

pip3 uninstall community-tulip-api -y >/dev/null
echo "Uninstalled existing community-tulip-api installation."

pip3 install $(ls -AU | head -1) >/dev/null
echo "Installed new community-tulip-api build."
