#!/bin/bash
# Launch Sioux Falls Network Simulation (24 intersections)

echo "=========================================="
echo "🚦 SIOUX FALLS NETWORK SIMULATION"
echo "=========================================="
echo ""
echo "Network: Sioux Falls (24 nodes, 76 edges)"
echo "Based on real transportation network!"
echo ""
echo "Vehicle Distribution:"
echo "  🚗 ~680 cars across ENTIRE network"
echo "  🚗 25 different routes covering all areas"
echo "  🚗 North, South, East, West, Central flows"
echo "  🚗 All vehicles are BLUE CARS"
echo ""
echo "Vehicles on EVERY part of the network!"
echo "=========================================="
echo "Controls:"
echo "  ▶️  Play: Click green triangle"
echo "  ⏸️  Pause: Press SPACE"
echo "  🔍 Zoom: Mouse wheel / Ctrl+F"
echo "  ⏱️  Speed: Adjust Delay slider"
echo "=========================================="
echo ""
echo "Opening SUMO..."

cd "$(dirname "$0")"
sumo-gui --configuration-file sioux_falls.sumocfg
