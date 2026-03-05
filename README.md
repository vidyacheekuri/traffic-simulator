# 🚦 Traffic Simulator for Cybersecurity Training

**Supported by NSF** | SUMO + TraCI | Python

A traffic simulation platform for studying and demonstrating cyber attacks on traffic infrastructure. Includes vehicle and pedestrian flows with adaptive and pedestrian-actuated traffic light control.

---

## 🚀 QUICK START

### 1. Simple Intersection (vehicles only)
```bash
./START_DEMO.sh
```

### 2. Simple Intersection + Pedestrians (static timing)
```bash
./START_PED_DEMO.sh
```

### 3. Pedestrian-Actuated Traffic Lights (green only when peds waiting)
```bash
./RUN_PED_ACTUATED.sh
```
*Requires `SUMO_HOME` to be set.*

### 4. Sioux Falls Network (adaptive, queue-based control)
```bash
./sioux_falls/RUN_SIOUX_FALLS.sh
```

### 5. Sioux Falls Adaptive Controller (TraCI)
```bash
./sioux_falls/RUN_ADAPTIVE.sh
```

Click the ▶️ Play button in SUMO to run!

---

## 📋 WHAT WE BUILT

### Simple 4-Way Intersection
- Network with traffic lights and coordinated phases
- 270 vehicles, 8 flows (N-S, E-W, turns)
- IDM car-following model
- Good for learning SUMO basics

### Pedestrian Crossings
- Sidewalks and 4 pedestrian crossings at the intersection
- Person flows (N-S, S-N, E-W, W-E) with configurable periods
- Pedestrian phases in traffic light program

### Pedestrian-Actuated Controller (`ped_actuated_controller.py`)
- **Detection:** Uses TraCI to detect peds waiting at crossings (`getWaitingTime`, `getNextEdge`, `getLastStepPersonIDs`)
- **Logic:** Pedestrian green only when someone is waiting (after min vehicle green)
- **Control:** Direct state control via `setRedYellowGreenState` for reliable switching
- **Parameters:** MIN_VEHICLE_GREEN=15s, MAX_GREEN=60s

### Vehicle-Actuated Controller (`sioux_falls/traffic_light_controller.py`)
- Queue-based extension: extends green when vehicles are waiting
- MIN_GREEN=5s, MAX_GREEN=60s, YELLOW=3s, EXTENSION=3s
- Uses `getLastStepHaltingNumber()` for queue detection

### Sioux Falls Network
- Real-world research network (24 nodes, 76 edges)
- Converted from GraphML via `convert_sioux_to_sumo.py`
- Multiple vehicle flows and OD pairs

---

## 📁 PROJECT STRUCTURE

| File / Folder | Description |
|---------------|-------------|
| `simple_intersection.*` | 4-way intersection (vehicles only) |
| `simple_intersection_ped.*` | Same intersection + sidewalks + pedestrian crossings |
| `ped_actuated_controller.py` | TraCI controller for pedestrian-actuated signals |
| `simple_gui.xml` | SUMO GUI display settings |
| `sioux_falls/` | Sioux Falls network, adaptive controller, conversion scripts |

---

## 🛠️ REQUIREMENTS

- [SUMO](https://eclipse.dev/sumo/) (Simulation of Urban Mobility)
- Python 3
- `SUMO_HOME` environment variable set (for TraCI scripts)

---

## 🎮 CONTROLS

- **▶️ Play:** Click green triangle or press SPACE
- **⏸️ Pause:** SPACE
- **🔍 Zoom:** Mouse wheel or Ctrl+F
- **👆 Pan:** Right-click + drag
- **⏱️ Speed:** Adjust "Delay (ms)" slider

---

## 📚 REFERENCES

- [SUMO Documentation](https://sumo.dlr.de/docs/)
- [TraCI Tutorial](https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html)
- [TraCI Pedestrian Crossing](https://sumo.dlr.de/docs/Tutorials/TraCIPedCrossing.html)
