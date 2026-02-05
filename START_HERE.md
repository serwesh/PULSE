# Quick Start Guide - PDW Simulator

## How to View This Documentation

If you're seeing this properly formatted, the markdown viewer is working!

---

## Summary: Data Generation & Noise Addition

### How Data is Generated:
1. Load configuration from `dataconfig.yaml`
2. Create 5 radars and 1 sensor
3. Calculate trajectories and pulse times
4. For each pulse: Calculate true values → Check detection → Add noise → Save

### How Noise is Added:
**Formula:** Measured Value = True Value + Systematic Error + Random Error

**Current Configuration:**
- Amplitude: ±2 dBm (Gaussian)
- TOA: ±5 ns (Gaussian)
- Frequency: ±1% (Gaussian)
- Pulse Width: ±25 ns (Gaussian)
- AOA: ±3.5° (Gaussian)

---

## Files to Read:

1. **PDW_Documentation.html** - Open in browser (double-click)
2. **SUMMARY.txt** - Plain text version
3. **Figure1_PDW_Workflow.png** - Workflow diagram
4. **Figure2_Error_Model.png** - Error model diagram

---

## Keyboard Shortcuts for Markdown Preview:

- **Ctrl+Shift+V** - Open preview
- **Ctrl+K V** - Open preview to the side

---

## Key Code Locations:

**Noise is added here:**
- File: `src/pdw_simulator/sensor_properties.py`
- Functions: `measure_amplitude()`, `measure_toa()`, `measure_frequency()`, etc.

**Noise parameters configured here:**
- File: `dataconfig.yaml` (lines 156-190)

---

For complete details, see:
- DATA_GENERATION_EXPLAINED.md
- QUICK_REFERENCE_NOISE.md
- REPORT_FIGURES.md
