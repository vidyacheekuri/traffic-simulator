# 🚦 Traffic Light Simulations - SUMO

## 🚀 QUICK START:

### **1. Simple Intersection (Learning):**
```bash
./START_DEMO.sh
```

### **2. 2x3 Grid (Advanced - 6 Intersections):**
```bash
./RUN_GRID_2X3.sh
```

### **3. Sioux Falls Network (Professional - 24 Nodes):**
```bash
./sioux_falls/RUN_SIOUX_FALLS.sh
```

Then click the ▶️ Play button in SUMO!

---

## 📁 FILES (7 Total - Super Clean!)

### **To Run:**
- `START_DEMO.sh` ⭐ **Run this script!**

### **SUMO Simulation Files:**
- `simple_intersection.net.xml` - The intersection network
- `simple_intersection.rou.xml` - Vehicle routes (270 vehicles)
- `simple_intersection.sumocfg` - Main configuration
- `simple_gui.xml` - Display settings (zoom, delay)

### **Documentation:**
- `README.md` - This file
- `QUICK_REFERENCE.txt` - Control shortcuts

---

## 📊 SIMULATIONS AVAILABLE:

### **1. Simple Intersection** (`./START_DEMO.sh`)
- 1 intersection with traffic lights
- 270 vehicles (single vehicle type)
- 8 traffic flows
- **Good for:** Learning basics

### **2. 2x3 Grid Network** (`./RUN_GRID_2X3.sh`)
- **6 intersections** (2 rows × 3 columns)
- **~650 vehicles** with **4 vehicle types:**
  - 🚗 Cars (blue) - Fast
  - 🚚 Trucks (brown) - Slow & heavy
  - 🚌 Buses (orange) - Medium
  - 🏍️ Motorcycles (magenta) - Very fast
- **14 traffic flows** (horizontal, vertical, diagonal)
- **Good for:** Advanced demonstration

### **3. Sioux Falls Network** (`./sioux_falls/RUN_SIOUX_FALLS.sh`)
- **24 intersections** (real-world network)
- **76 edges** (roads connecting nodes)
- **55 vehicles** with **3 OD pairs:**
  - 🔵 Blue: Node 1 → 24 (35 vehicles)
  - 🩷 Pink: Node 10 → 20 (10 vehicles)
  - 🟣 Purple: Node 19 → 13 (10 vehicles)
- **Standard research network** used worldwide
- **Good for:** Professional demonstration & research

---

## 🎮 CONTROLS:

- **▶️ Play:** Click green triangle or press SPACE
- **⏸️ Pause:** Press SPACE
- **🔍 Zoom:** Mouse wheel or Ctrl+F to fit
- **👆 Pan:** Right-click + drag
- **⏱️ Speed:** Adjust "Delay (ms)" slider (0=fastest, 500=slowest)

---

## ✅ WHAT YOU BUILT:

1. ✅ 4-way intersection network from scratch
2. ✅ Traffic light system with coordinated phases
3. ✅ 270 vehicles with realistic IDM car-following
4. ✅ Multiple routes (straight & turning movements)
5. ✅ Professional SUMO simulation

---

**Ready for your meeting! Run `./START_DEMO.sh` now!** 🚀
