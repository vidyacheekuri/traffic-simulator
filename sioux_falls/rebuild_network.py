#!/usr/bin/env python3
"""Rebuild Sioux Falls network with wider lanes (fixes vehicles occupying 2 lanes)."""
import subprocess
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("1. Converting GraphML to SUMO...")
subprocess.run(["python3", "convert_sioux_compact.py"], check=True)

print("\n2. Building network with WIDER LANES (4.5m)...")
result = subprocess.run([
    "netconvert",
    "--node-files=sioux_falls.nod.xml",
    "--edge-files=sioux_falls.edg.xml",
    "--output-file=sioux_falls.net.xml",
    "--tls.guess",
    "--default.lanewidth", "4.5"  # Wider lanes so cars fit properly
], capture_output=True, text=True)

if result.returncode != 0:
    print("Error:", result.stderr)
    exit(1)
print("✓ Network rebuilt with wider lanes!")
