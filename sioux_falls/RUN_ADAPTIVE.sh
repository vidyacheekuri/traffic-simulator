#!/bin/bash
# Launch Sioux Falls with ADAPTIVE traffic lights (TraCI controller)

echo "=========================================="
echo "🚦 ADAPTIVE TRAFFIC SIGNALS"
echo "=========================================="
echo ""
echo "  • Dynamic durations based on queue length"
echo "  • MIN_GREEN=5s | MAX_GREEN=60s"
echo "  • Edit traffic_light_controller.py for settings"
echo ""
echo "=========================================="

cd "$(dirname "$0")"
python3 traffic_light_controller.py
