# 🚦 Sioux Falls Network Simulation

## 🚀 QUICK START:
```bash
./RUN_SIOUX_FALLS.sh
```
Then click ▶️ Play!

---

## 📊 WHAT IS SIOUX FALLS?

The **Sioux Falls network** is a **real-world transportation test network** commonly used in traffic research. It represents the city of Sioux Falls, South Dakota.

### **Network Stats:**
- ✅ **24 nodes** (intersections)
- ✅ **76 edges** (roads/links)
- ✅ **Traffic lights at major intersections**
- ✅ Based on actual city street layout

This is a **standard benchmark** network used in transportation engineering research worldwide!

---

## 🎯 THIS SIMULATION:

### **Vehicle Flows** (Matching Original Python Simulation):

1. **🔵 Blue Flow:** Node 1 → Node 24
   - **35 vehicles**
   - Route: Through the network from northwest to southeast
   
2. **🩷 Pink Flow:** Node 10 → Node 20
   - **10 vehicles**
   - Route: Through central network
   
3. **🟣 Purple Flow:** Node 19 → Node 13
   - **10 vehicles**
   - Route: Across the network

**Total: 55 vehicles** with realistic IDM car-following behavior

---

## 🗺️ NETWORK LAYOUT:

```
          1
         /|\
        / | \
       /  |  \
      2   3   6
         \|  /|\
          12   ...
          |
         13
          |
         24
```

*Simplified view - actual network has 24 nodes interconnected*

---

## 📈 COMPARISON: Python vs. SUMO

| Feature | Python Simulation | SUMO Simulation |
|---------|-------------------|-----------------|
| **Network** | Sioux Falls (24 nodes) | Sioux Falls (24 nodes) |
| **Visualization** | Matplotlib (2D plot) | SUMO-GUI (professional) |
| **Traffic Lights** | Custom implementation | Built-in SUMO logic |
| **Vehicle Model** | Custom IDM | SUMO IDM (validated) |
| **Performance** | Moderate | Fast (C++ engine) |
| **Realism** | Good | Professional-grade |

---

## 🔧 FILES CREATED:

### **Conversion:**
- `convert_sioux_to_sumo.py` - Python script to convert GraphML → SUMO
- `sioux_falls.nod.xml` - 24 nodes with coordinates
- `sioux_falls.edg.xml` - 76 edges with properties

### **SUMO Network:**
- `sioux_falls.net.xml` - Compiled SUMO network (auto-generated traffic lights)

### **Simulation:**
- `sioux_falls.rou.xml` - 3 vehicle flows (55 vehicles)
- `sioux_falls.sumocfg` - Main configuration
- `sioux_falls_gui.xml` - Display settings

### **Launch:**
- `RUN_SIOUX_FALLS.sh` - **Run this script!**

---

## 🎮 CONTROLS:

- **▶️ Start:** Click green triangle or SPACE
- **⏸️ Pause:** Press SPACE
- **🔍 Zoom:** Mouse wheel / Press Ctrl+F to fit
- **👆 Pan:** Right-click + drag
- **⏱️ Speed:** Adjust "Delay (ms)" slider

---

## 💡 WHAT TO OBSERVE:

### **Network Complexity:**
- **24 intersections** with coordinated traffic lights
- **Multiple paths** between origins and destinations
- **Realistic urban network** topology

### **Traffic Dynamics:**
- **Route choice** - SUMO finds shortest paths automatically
- **Traffic light coordination** - Vehicles must wait at reds
- **Congestion propagation** - Queues form and clear
- **Realistic speeds** - Based on actual free-flow times

### **Vehicle Behavior:**
- **IDM car-following** - Safe distances maintained
- **Smooth acceleration/deceleration**
- **Queue formation and dispersal**
- **Color-coded flows** for easy tracking

---

## 📚 ACADEMIC CONTEXT:

**Sioux Falls Network:**
- Introduced in 1980s by transportation researchers
- Standard test network for traffic assignment algorithms
- Used in hundreds of research papers
- Real-world validated parameters

**Why Use It?**
- ✅ Complex enough to be realistic
- ✅ Simple enough to understand
- ✅ Well-documented and standardized
- ✅ Comparable to other research

---

## 🎓 WHAT YOU LEARNED:

1. ✅ **Converting real networks** - GraphML → SUMO format
2. ✅ **Large-scale simulation** - 24 intersections with traffic lights
3. ✅ **Professional tools** - Using industry-standard test networks
4. ✅ **Research methods** - Replicating standard benchmarks
5. ✅ **Validation** - Comparing Python vs. SUMO implementations

---

## 📊 ALL SIMULATIONS COMPARISON:

| Simulation | Intersections | Vehicle Types | Vehicles | Complexity |
|------------|--------------|---------------|----------|------------|
| **Simple** | 1 | 1 generic | 270 | Basic |
| **2x3 Grid** | 6 | 4 types | ~650 | Advanced |
| **Sioux Falls** | 24 | 1 generic | 55 | Professional |

---

## 🚀 NEXT STEPS:

### **Easy Enhancements:**
- Increase traffic volume (500+ vehicles)
- Add more OD pairs
- Different time-of-day patterns

### **Advanced:**
- Traffic signal optimization
- Route choice analysis
- Congestion pricing scenarios
- Real-time traffic management

---

**Run the simulation now:**
```bash
./RUN_SIOUX_FALLS.sh
```

**This is the same network as your Python simulation - now in professional SUMO!** 🎉
