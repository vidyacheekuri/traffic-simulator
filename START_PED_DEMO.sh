#!/bin/bash
# Simple 4-way intersection with PEDESTRIANS (ped green/red at crossing)

echo "=========================================="
echo "🚶 4-WAY INTERSECTION + PEDESTRIANS"
echo "=========================================="
echo ""
echo "  • Vehicles: 4 directions + turns"
echo "  • Pedestrians: N-S, S-N, E-W, W-E crossings"
echo "  • Ped phases: Green = walk, Red = wait"
echo ""
echo "For cybersec training: attack ped signals!"
echo "=========================================="

cd "$(dirname "$0")"
sumo-gui --configuration-file simple_intersection_ped.sumocfg
