#!/usr/bin/env python3
"""
Pedestrian-Actuated Traffic Light Controller (TraCI)
====================================================
Pedestrian green activates ONLY when pedestrians are detected waiting.
Otherwise vehicles keep green (up to MAX_GREEN).

Uses setRedYellowGreenState for full control (bypasses phase program).

Run: python3 ped_actuated_controller.py
      (or ./RUN_PED_ACTUATED.sh)
"""

import os
import sys

# SUMO tools
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.exit("Set SUMO_HOME to your SUMO installation")
import traci

# ============================================================
# PEDESTRIAN-ACTUATED SETTINGS
# ============================================================

TLSID = 'center'
MIN_VEHICLE_GREEN = 15   # Minimum green for vehicles before allowing ped-triggered switch (s)
MAX_GREEN = 60           # Max green before forced switch (s)
PED_WAIT_THRESHOLD = 1   # Seconds a ped must wait to "push button"
STEP_LENGTH = 0.1        # Must match sumocfg

# State strings (24 chars: 20 vehicle links + 4 ped links 20-23)
# Links 20-21-22-23: w1->c0, w2->c1, w3->c2, w0->c3 (N-S, E-W, N-S, E-W)
STATE_NS_VEH_PED_EW = "gGGggrrrrrgGGggrrrrrrGrG"  # NS green, E-W peds green
STATE_NS_TRANSITION = "gGGggrrrrrgGGggrrrrrrrrr"  # NS green, all ped red
STATE_NS_YELLOW = "yyyyyrrrrryyyyyrrrrrrrrr"     # Yellow NS
STATE_EW_VEH_PED_NS = "rrrrrgGGggrrrrrgGGggGrGr"  # EW green, N-S peds green
STATE_EW_TRANSITION = "rrrrrgGGggrrrrrgGGggrrrr"  # EW green, all ped red
STATE_EW_YELLOW = "rrrrryyyyyrrrrryyyyyrrrr"     # Yellow EW

TRANSITION_DURATION = 5   # seconds
YELLOW_DURATION = 3       # seconds

# Walking areas where peds wait before crossing
WALKING_AREAS = [':center_w0', ':center_w1', ':center_w2', ':center_w3']

# Crossings: N-S = c0, c2; E-W = c1, c3
CROSSINGS_NS = [':center_c0', ':center_c2']   # Peds need EW vehicle phase
CROSSINGS_EW = [':center_c1', ':center_c3']     # Peds need NS vehicle phase


def check_waiting_pedestrians():
    """
    Check if any pedestrian is waiting to cross (pushed the button).
    Returns: ('ns',) if N-S peds waiting, ('ew',) if E-W peds waiting, None otherwise.
    """
    ns_waiting = False
    ew_waiting = False

    for edge_id in WALKING_AREAS:
        try:
            peds = traci.edge.getLastStepPersonIDs(edge_id)
        except traci.exceptions.TraCIException:
            continue
        for ped in peds:
            try:
                wait_time = traci.person.getWaitingTime(ped)
                next_edge = traci.person.getNextEdge(ped)
            except (traci.exceptions.TraCIException, AttributeError):
                continue
            if next_edge is None:
                continue
            # Ped has been waiting and next step is a crossing
            if wait_time >= PED_WAIT_THRESHOLD:
                if next_edge in CROSSINGS_NS:
                    ns_waiting = True
                elif next_edge in CROSSINGS_EW:
                    ew_waiting = True
    if ns_waiting:
        return 'ns'
    if ew_waiting:
        return 'ew'
    return None


def run():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg = os.path.join(script_dir, 'simple_intersection_ped.sumocfg')
    if not os.path.exists(cfg):
        print(f"Error: Config not found: {cfg}")
        sys.exit(1)

    sumo_bin = 'sumo-gui'
    sumo_cmd = [sumo_bin, '-c', cfg, '--start']
    if '--nogui' in sys.argv:
        sumo_bin = 'sumo'
        sumo_cmd = [sumo_bin, '-c', cfg]

    print("=" * 55)
    print("  Pedestrian-Actuated Traffic Lights (TraCI)")
    print("=" * 55)
    print("  Ped green ONLY when pedestrians are waiting.")
    print(f"  MIN_VEHICLE_GREEN: {MIN_VEHICLE_GREEN}s | MAX_GREEN: {MAX_GREEN}s")
    print("=" * 55)
    print("\nRunning... Close SUMO or Ctrl+C to stop\n")

    traci.start(sumo_cmd)

    # Use direct state control - bypass phase program entirely
    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_VEH_PED_EW)

    state = 'ns_green'       # ns_green | ns_transition | ns_yellow | ew_green | ew_transition | ew_yellow
    time_in_state = 0.0
    active_request = False
    max_steps = 6000

    try:
        step = 0
        while step < max_steps and traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            time_in_state += STEP_LENGTH

            # Check for waiting peds (only in main green phases)
            if state == 'ns_green' and not active_request:
                if check_waiting_pedestrians() == 'ns':
                    active_request = True
            elif state == 'ew_green' and not active_request:
                if check_waiting_pedestrians() == 'ew':
                    active_request = True

            # State machine
            if state == 'ns_green':
                if (time_in_state > MIN_VEHICLE_GREEN and active_request) or time_in_state >= MAX_GREEN:
                    state = 'ns_transition'
                    time_in_state = 0.0
                    active_request = False
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_TRANSITION)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_VEH_PED_EW)

            elif state == 'ns_transition':
                if time_in_state >= TRANSITION_DURATION:
                    state = 'ns_yellow'
                    time_in_state = 0.0
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_YELLOW)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_TRANSITION)

            elif state == 'ns_yellow':
                if time_in_state >= YELLOW_DURATION:
                    state = 'ew_green'
                    time_in_state = 0.0
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_VEH_PED_NS)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_YELLOW)

            elif state == 'ew_green':
                if (time_in_state > MIN_VEHICLE_GREEN and active_request) or time_in_state >= MAX_GREEN:
                    state = 'ew_transition'
                    time_in_state = 0.0
                    active_request = False
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_TRANSITION)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_VEH_PED_NS)

            elif state == 'ew_transition':
                if time_in_state >= TRANSITION_DURATION:
                    state = 'ew_yellow'
                    time_in_state = 0.0
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_YELLOW)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_TRANSITION)

            elif state == 'ew_yellow':
                if time_in_state >= YELLOW_DURATION:
                    state = 'ns_green'
                    time_in_state = 0.0
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_NS_VEH_PED_EW)
                else:
                    traci.trafficlight.setRedYellowGreenState(TLSID, STATE_EW_YELLOW)

            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nStopped by user.")

    traci.close()
    print("\nDone!")


if __name__ == "__main__":
    run()
