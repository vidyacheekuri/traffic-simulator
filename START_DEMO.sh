#!/bin/bash
# Simple script to start the intersection demo

echo "=========================================="
echo "Starting Simple Intersection Demo"
echo "=========================================="
echo ""
echo "SUMO-GUI Controls:"
echo "  - Click ▶ (Play) to start"
echo "  - Press SPACE to pause/resume"
echo "  - Mouse wheel to zoom"
echo "  - Ctrl+F to fit view"
echo ""
echo "Opening SUMO..."
echo "=========================================="

cd /Users/vidyacheekuri/Local_Storage/Traffic_simulator

# Start SUMO-GUI (no quit-on-end, so it stays open)
sumo-gui --configuration-file simple_intersection.sumocfg
