#!/usr/bin/env bash

set -euo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

make install
make migrate
make compilemessages
make collectstatic
