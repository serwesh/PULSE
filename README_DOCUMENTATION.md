# 📚 Complete Documentation Index

## Welcome! 👋

I've created comprehensive documentation to help you understand how data is generated and how noise is added in the PDW simulator. Here's what's available:

---

## 📖 Documentation Files

### 1. **DATA_GENERATION_EXPLAINED.md** ⭐⭐⭐
**Best for:** Complete beginners who want to understand everything from scratch

**Contents:**
- What is a PDW simulator?
- Complete file structure overview
- Step-by-step data generation process
- Detailed explanation of noise addition
- Types of error models (Gaussian, Uniform, etc.)
- Visual explanations and examples
- Common questions and answers

**Start here if:** You're new to the project and want a thorough understanding

---

### 2. **QUICK_REFERENCE_NOISE.md** ⭐⭐
**Best for:** Quick lookups and code references

**Contents:**
- Exact code snippets for each noise function
- Configuration examples
- How to change noise levels
- Tracing a single pulse through the code
- Learning exercises

**Start here if:** You understand the basics and need to find specific code

---

### 3. **Visual Diagrams** 🎨

#### **pdw_data_flow_diagram.png**
Shows the complete flow from configuration to output:
- Configuration phase
- Simulation loop
- Detection check
- Noise addition
- Output generation
- Gaussian distribution visualization

#### **noise_types_visualization.png**
Shows different types of errors:
- Constant error
- Linear error
- Sinusoidal error
- Gaussian error
- Uniform error

---

## 🗂️ Important Project Files

### Core Simulation Files:

1. **`src/pdw_simulator/main.py`**
   - Main simulation loop
   - Orchestrates everything
   - Lines 66-283: `run_simulation()` function

2. **`src/pdw_simulator/models.py`**
   - Radar class (lines 24-285)
   - Sensor class (lines 288-355)
   - Defines all properties and behaviors

3. **`src/pdw_simulator/sensor_properties.py`** ⭐ NOISE IS HERE!
   - Line 7-56: `create_error_model()` - Creates error functions
   - Line 80-99: `detect_pulse()` - Probabilistic detection
   - Line 126-157: `measure_amplitude()` - Amplitude with noise
   - Line 214-246: `measure_toa()` - TOA with noise
   - Line 249-284: `measure_frequency()` - Frequency with noise
   - Line 287-317: `measure_pulse_width()` - Pulse width with noise
   - Line 320-344: `measure_aoa()` - AOA with noise

4. **`src/pdw_simulator/radar_properties.py`**
   - PRI generation functions
   - Frequency generation functions
   - Pulse width generation functions
   - Antenna pattern calculations

5. **`src/pdw_simulator/scenario_geometry_functions.py`**
   - Trajectory calculations
   - Position updates
   - Geometric calculations

### Configuration Files:

6. **`dataconfig.yaml`** ⭐ NOISE PARAMETERS HERE!
   - Lines 1-5: Scenario settings
   - Lines 7-145: Radar configurations (5 radars)
   - Lines 146-191: Sensor configurations (1 sensor)
     - Lines 156-162: Amplitude error settings
     - Lines 163-169: TOA error settings
     - Lines 170-176: Frequency error settings
     - Lines 177-183: Pulse width error settings
     - Lines 184-190: AOA error settings

7. **`config/systemconfig.yaml`**
   - System-level settings
   - Output directory configuration

---

## 🎯 Quick Start Guide

### For Complete Beginners:

1. **Read:** `DATA_GENERATION_EXPLAINED.md`
   - Start from the top
   - Read each section carefully
   - Look at the diagrams

2. **Explore:** Open the files mentioned
   - `src/pdw_simulator/sensor_properties.py`
   - `dataconfig.yaml`
   - Look at the code snippets mentioned in the docs

3. **Experiment:** Try changing noise parameters
   - Edit `dataconfig.yaml`
   - Change error values
   - Run simulation and observe changes

4. **Reference:** Use `QUICK_REFERENCE_NOISE.md`
   - When you need to find specific code
   - When you want to change something

---

## 🔍 Finding Specific Information

### "How is amplitude noise added?"
→ See `QUICK_REFERENCE_NOISE.md` - Section "Amplitude Noise"
→ Code: `sensor_properties.py`, lines 126-157

### "What types of noise are there?"
→ See `DATA_GENERATION_EXPLAINED.md` - Section "Types of Noise/Error Models"
→ Visual: `noise_types_visualization.png`

### "How does detection work?"
→ See `DATA_GENERATION_EXPLAINED.md` - Section "Step 2: Detection Check"
→ Code: `sensor_properties.py`, lines 80-99

### "How do I change noise levels?"
→ See `QUICK_REFERENCE_NOISE.md` - Section "How to Change Noise Levels"
→ Edit: `dataconfig.yaml`, sensor error sections

### "What's the complete flow?"
→ See `DATA_GENERATION_EXPLAINED.md` - Section "Summary - The Complete Flow"
→ Visual: `pdw_data_flow_diagram.png`

### "Where are pulses generated?"
→ See `DATA_GENERATION_EXPLAINED.md` - Section "Phase 1: Setup"
→ Code: `models.py`, lines 163-175 (calculate_pulse_times)
→ Code: `radar_properties.py` (PRI functions)

---

## 📊 Understanding the Data Flow

```
Configuration (YAML)
    ↓
Create Scenario, Radars, Sensors
    ↓
Calculate Trajectories & Pulse Times
    ↓
FOR EACH PULSE:
    ↓
Calculate TRUE values (perfect physics)
    ↓
Detection check (probabilistic)
    ↓
If detected:
    ↓
Add SYSTEMATIC noise (bias)
    ↓
Add ARBITRARY noise (random)
    ↓
Save MEASURED values
    ↓
Export to CSV
```

---

## 🎓 Learning Path

### Level 1: Understanding the Basics
1. Read `DATA_GENERATION_EXPLAINED.md` sections:
   - "What is This System?"
   - "Important Files Overview"
   - "How Data is Generated - Step by Step"

2. Look at diagrams:
   - `pdw_data_flow_diagram.png`

### Level 2: Understanding Noise
1. Read `DATA_GENERATION_EXPLAINED.md` sections:
   - "Step 3: Add Noise"
   - "Types of Noise/Error Models"
   - "Understanding Random Noise"

2. Look at diagrams:
   - `noise_types_visualization.png`

### Level 3: Code Deep Dive
1. Read `QUICK_REFERENCE_NOISE.md`
   - All sections

2. Open and study:
   - `sensor_properties.py`
   - `main.py` (run_simulation function)

### Level 4: Hands-On
1. Follow the "Learning Exercise" in `QUICK_REFERENCE_NOISE.md`
2. Modify `dataconfig.yaml`
3. Run simulations
4. Compare outputs

---

## 🛠️ Common Tasks

### Task: "I want to make the sensor more accurate"
1. Open `dataconfig.yaml`
2. Find the sensor section (line 146)
3. Reduce error values:
   ```yaml
   amplitude_error:
     arbitrary:
       error: "0.5 dBm"  # Was "2 dBm"
   ```
4. Save and run simulation

### Task: "I want to add systematic drift"
1. Open `dataconfig.yaml`
2. Find the error you want to modify
3. Change from constant to linear:
   ```yaml
   amplitude_error:
     systematic:
       type: "linear"
       error: "0 dBm"
       rate: "0.1 dBm/s"
   ```
4. Save and run simulation

### Task: "I want to understand what a specific function does"
1. Check `QUICK_REFERENCE_NOISE.md` for the function
2. Look at the code snippet
3. Read the "What it does" section
4. Check the configuration example

### Task: "I want to see the complete flow for one pulse"
1. Read `QUICK_REFERENCE_NOISE.md` - Section "Tracing a Single Pulse Through the Code"
2. Follow each step
3. Look at the actual code in the files mentioned

---

## 📝 Key Concepts Summary

### 1. True vs. Measured Values
- **True**: Perfect physics calculation (no noise)
- **Measured**: True value + noise (realistic)

### 2. Two Types of Noise
- **Systematic**: Consistent bias (same every time)
- **Arbitrary**: Random variation (different each time)

### 3. Error Models
- **Constant**: Fixed offset
- **Linear**: Increases over time
- **Sinusoidal**: Periodic variation
- **Gaussian**: Random (bell curve) - MOST COMMON
- **Uniform**: Random (flat distribution)

### 4. Detection is Probabilistic
- Strong signals: Always detected
- Weak signals: Sometimes missed
- Based on amplitude and probability thresholds

### 5. Configuration Controls Everything
- All noise parameters in `dataconfig.yaml`
- Easy to modify without changing code
- Each sensor can have different error characteristics

---

## 🎯 Remember

1. **Start with the overview** (`DATA_GENERATION_EXPLAINED.md`)
2. **Use the quick reference** when you need specific code
3. **Look at the diagrams** to visualize the process
4. **Experiment** by changing configuration values
5. **Ask questions** if something is unclear

---

## 📞 Need More Help?

If you're stuck or confused:

1. **Re-read the relevant section** in the documentation
2. **Look at the code** mentioned in the docs
3. **Try the learning exercises** in `QUICK_REFERENCE_NOISE.md`
4. **Experiment** with small changes to see what happens

---

## 🎉 You're Ready!

You now have:
- ✅ Complete explanation of data generation
- ✅ Detailed noise addition documentation
- ✅ Visual diagrams
- ✅ Code references
- ✅ Configuration examples
- ✅ Learning exercises

**Start with `DATA_GENERATION_EXPLAINED.md` and work your way through!**

Good luck! 🚀
