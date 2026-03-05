#!/bin/bash
# Pedestrian-actuated traffic lights - green only when peds are waiting

cd "$(dirname "$0")"
echo "Pedestrian-actuated mode: ped green only when people are at the crossing."
python3 ped_actuated_controller.py "$@"
