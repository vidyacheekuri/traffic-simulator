#!/usr/bin/env python3
"""
Adaptive Traffic Light Controller with TraCI
=============================================
Dynamic signal durations based on incoming traffic.

Based on: https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html

Run: cd sioux_falls && python3 traffic_light_controller.py
"""

import traci
import sys
import os

# ============================================================
# ADAPTIVE SIGNAL SETTINGS (real-world constraints)
# ============================================================

MIN_GREEN = 5       # Minimum green time (s) - never interrupt before this
MAX_GREEN = 60      # Maximum green time (s) - force switch after this
YELLOW_DURATION = 3 # Yellow/all-red clearance (s) - do not interrupt
EXTENSION = 3       # Extra seconds when vehicles still waiting (s)

# ============================================================
# SIMULATION SETTINGS
# ============================================================

USE_GUI = True
SIMULATION_END = 600

# ============================================================
# ADAPTIVE LOGIC
# ============================================================

def get_lanes_with_green(tl_id):
    """Return set of incoming lane IDs that currently have green."""
    state = traci.trafficlight.getRedYellowGreenState(tl_id)
    links = traci.trafficlight.getControlledLinks(tl_id)
    green_lanes = set()
    for i, link_list in enumerate(links):
        if i < len(state) and state[i] in 'Gg':
            for (incoming, _, _) in link_list:
                if incoming:
                    green_lanes.add(incoming)
    return green_lanes

def get_halting_count(lane_ids):
    """Total number of stopped vehicles on given lanes."""
    return sum(traci.lane.getLastStepHaltingNumber(lid) for lid in lane_ids)

def is_green_phase(state):
    """Phase serves traffic (has green), not yellow/red clearance."""
    return 'G' in state or 'g' in state

def is_yellow_phase(state):
    """Phase is yellow/clearance - do not interrupt."""
    return 'y' in state or 'Y' in state

def apply_adaptive_control(tl_id, t, end_requested):
    """Adjust phase duration based on queue (actuated/adaptive logic)."""
    phase_idx = traci.trafficlight.getPhase(tl_id)
    state = traci.trafficlight.getRedYellowGreenState(tl_id)

    # Never interrupt yellow
    if is_yellow_phase(state):
        traci.trafficlight.setPhaseDuration(tl_id, YELLOW_DURATION)
        return False  # phase changed, reset end_requested

    if not is_green_phase(state):
        return False

    spent = traci.trafficlight.getSpentDuration(tl_id)
    green_lanes = get_lanes_with_green(tl_id)
    halted = get_halting_count(green_lanes)

    # Already decided to end - don't re-extend
    if end_requested:
        return True

    # Real-world: extend if queue not cleared, up to MAX_GREEN
    if halted > 0 and spent < MAX_GREEN and spent >= MIN_GREEN:
        new_duration = min(spent + EXTENSION, MAX_GREEN)
        traci.trafficlight.setPhaseDuration(tl_id, new_duration)
        return False
    elif spent >= MIN_GREEN and (halted == 0 or spent >= MAX_GREEN):
        traci.trafficlight.setPhaseDuration(tl_id, spent + 0.5)
        return True  # end requested
    else:
        if spent < MIN_GREEN:
            traci.trafficlight.setPhaseDuration(tl_id, MIN_GREEN)
        return False

# ============================================================
# MAIN
# ============================================================

def run_simulation():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_file = os.path.join(script_dir, "sioux_falls.sumocfg")
    if not os.path.exists(cfg_file):
        print(f"Error: Config file not found: {cfg_file}")
        sys.exit(1)

    sumo_cmd = ["sumo-gui" if USE_GUI else "sumo", "-c", cfg_file]
    if USE_GUI:
        sumo_cmd.append("--start")

    print("=" * 55)
    print("  Adaptive Traffic Light Controller (TraCI)")
    print("=" * 55)
    print(f"  MIN_GREEN: {MIN_GREEN}s | MAX_GREEN: {MAX_GREEN}s")
    print(f"  YELLOW: {YELLOW_DURATION}s | EXTENSION: {EXTENSION}s")
    print("=" * 55)
    print("\nRunning... Close SUMO or Ctrl+C to stop\n")

    traci.start(sumo_cmd)
    tl_ids = traci.trafficlight.getIDList()
    step = 0
    max_steps = int(SIMULATION_END / 0.1)
    end_requested = {tid: False for tid in tl_ids}
    prev_phase = {tid: -1 for tid in tl_ids}

    try:
        while step < max_steps:
            traci.simulationStep()
            step += 1
            t = traci.simulation.getTime()

            for tl_id in tl_ids:
                try:
                    phase = traci.trafficlight.getPhase(tl_id)
                    if phase != prev_phase[tl_id]:
                        end_requested[tl_id] = False
                        prev_phase[tl_id] = phase

                    end_requested[tl_id] = apply_adaptive_control(
                        tl_id, t, end_requested[tl_id]
                    )
                except Exception:
                    pass

            if step % 500 == 0:
                n = traci.vehicle.getIDCount()
                print(f"  Time: {t:6.1f}s | Vehicles: {n:3d}")

    except KeyboardInterrupt:
        print("\nStopped by user.")

    traci.close()
    print("\nDone!")

if __name__ == "__main__":
    run_simulation()
