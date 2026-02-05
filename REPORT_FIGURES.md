# Report Figures - PDW Simulator

## Professional Diagrams for Project Report

This document contains the figure captions and descriptions for the two main diagrams created for your PDW simulator project report.

---

## Figure 1: PDW Simulation Workflow

**File:** `Figure1_PDW_Workflow.png`

### Figure Caption:
```
Figure 1: Complete workflow of the PDW (Pulse Descriptor Word) simulation system showing 
four main phases: (1) Configuration & Initialization, (2) Simulation Loop with true 
parameter calculation, (3) Measurement with noise addition, and (4) Data export. The 
system processes radar pulses from 5 emitters detected by 1 sensor, applying realistic 
measurement errors before output generation.
```

### Detailed Description for Report:

The PDW simulation workflow consists of four distinct phases as illustrated in Figure 1:

**Phase 1 - Configuration & Initialization:** The simulation begins by loading configuration parameters from `dataconfig.yaml`, which defines the scenario timeline (t=0 to 100s with Δt=0.01s time steps). The system initializes 5 radar emitters and 1 sensor, each with specific properties. Radars are configured with position, velocity, transmit power (in dBm), PRI (Pulse Repetition Interval) type, operating frequency, pulse width, and antenna pattern characteristics. The sensor is configured with position, velocity, detection probability levels, and error models for each measurement parameter. Following initialization, the system calculates trajectories for all entities and generates pulse emission times based on each radar's PRI configuration.

**Phase 2 - Simulation Loop:** For each emitted radar pulse, the system employs vectorized processing to calculate true physical parameters. The distance between radar and sensor is computed using Euclidean geometry: d = √[(xs-xr)² + (ys-yr)²]. The angle of arrival is determined using θ = arctan2(ys-yr, xs-xr). The received amplitude incorporates transmit power (P₀), antenna gain G(θ) based on the relative angle, and path loss following the inverse square law: P = P₀ + G(θ) - 20log₁₀(d). Time of arrival (TOA) accounts for propagation delay: TOA = t + d/c, where c is the speed of light. Frequency measurements include Doppler shift effects: f = f₀ + Δf_doppler. A probabilistic detection check determines whether the sensor successfully detects each pulse based on signal strength and configured detection probability levels.

**Phase 3 - Measurement with Noise:** Detected pulses undergo realistic measurement error modeling. Each parameter (amplitude, TOA, frequency, pulse width, and AOA) is corrupted by two error components: systematic error (εsys) and arbitrary error (Gaussian noise). The measurement equations are:
- Amplitude: Pmeas = Ptrue + εsys + N(0, 2dBm)
- TOA: tmeas = ttrue + εsys + N(0, 5ns)
- Frequency: fmeas = ftrue + εsys + N(0, 1%)
- Pulse Width: PWmeas = PWtrue + εsys + N(0, 25ns)
- AOA: θmeas = θtrue + εsys + N(0, 3.5°)

where N(μ, σ) represents Gaussian noise with mean μ and standard deviation σ.

**Phase 4 - Output:** All detected and measured PDWs are aggregated and exported to CSV format with columns: Name (radar identifier), Freq(MHz), PW(µs), Azimuth(°), Power(dBm), and PRI.

---

## Figure 2: Sensor Measurement Error Model

**File:** `Figure2_Error_Model.png`

### Figure Caption:
```
Figure 2: Architecture of the sensor measurement error model showing systematic and 
arbitrary error components. The model implements five error types (constant, linear, 
sinusoidal, Gaussian, and uniform) with parameter-specific configurations. The Gaussian 
distribution visualization shows the 68-95-99.7 rule, and the detection probability 
table defines signal-dependent detection thresholds.
```

### Detailed Description for Report:

The sensor measurement error model (Figure 2) implements a comprehensive framework for simulating realistic measurement uncertainties in radar signal detection and parameter estimation.

**Error Model Framework:** The model distinguishes between two fundamental error categories:

1. **Systematic Error (εsys):** Predictable, deterministic errors that remain consistent across measurements. Three models are supported:
   - Constant: ε(t) = C, representing fixed calibration offsets
   - Linear: ε(t) = C + R·t, modeling sensor drift over time
   - Sinusoidal: ε(t) = A·sin(2πf·t + φ), capturing periodic interference effects

2. **Arbitrary Error (εarb):** Stochastic errors varying randomly between measurements:
   - Gaussian: ε ~ N(0, σ²), following a normal distribution with zero mean and variance σ²
   - Uniform: ε ~ U(-a, +a), with equal probability across the range [-a, +a]

**Measurement Equation:** The fundamental measurement equation combines true values with both error components:

```
Measured Value = True Value + εsys + εarb
```

This equation applies uniformly to all measured parameters (amplitude, TOA, frequency, pulse width, and AOA).

**Configured Error Parameters:** The current implementation uses the following configuration:

| Parameter    | Systematic Error | Arbitrary Error        |
|--------------|------------------|------------------------|
| Amplitude    | Constant: 0 dBm  | Gaussian: σ = 2 dBm    |
| TOA          | Constant: 0 s    | Gaussian: σ = 5 ns     |
| Frequency    | Constant: 0 Hz   | Gaussian: σ = 1%       |
| Pulse Width  | Constant: 0 s    | Gaussian: σ = 25 ns    |
| AOA          | Constant: 0°     | Gaussian: σ = 3.5°     |

All systematic errors are configured as constant with zero bias, meaning the current model focuses on arbitrary (random) measurement uncertainties.

**Gaussian Error Distribution:** The Gaussian distribution follows the empirical rule (68-95-99.7 rule):
- 68.2% of measurements fall within ±1σ of the true value
- 95.4% of measurements fall within ±2σ of the true value
- 99.7% of measurements fall within ±3σ of the true value

This statistical behavior ensures realistic measurement scatter consistent with physical sensor limitations.

**Detection Probability Model:** Signal detection is probabilistic, dependent on received signal strength:

| Signal Level (dBm) | Detection Probability |
|--------------------|-----------------------|
| > -65              | 100%                  |
| -65 to -70         | 100%                  |
| -70 to -75         | 90%                   |
| -75 to -80         | 70%                   |
| < -80              | 50%                   |

Signals above the saturation level (-65 dBm) are always detected, while weaker signals have progressively lower detection probabilities, simulating realistic receiver sensitivity characteristics.

---

## Usage in Report

### LaTeX Example:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{Figure1_PDW_Workflow.png}
    \caption{Complete workflow of the PDW (Pulse Descriptor Word) simulation system 
    showing four main phases: (1) Configuration \& Initialization, (2) Simulation Loop 
    with true parameter calculation, (3) Measurement with noise addition, and 
    (4) Data export.}
    \label{fig:pdw_workflow}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{Figure2_Error_Model.png}
    \caption{Architecture of the sensor measurement error model showing systematic and 
    arbitrary error components with parameter-specific configurations.}
    \label{fig:error_model}
\end{figure}
```

### Microsoft Word:
1. Insert → Pictures → Select `Figure1_PDW_Workflow.png`
2. Right-click → Insert Caption
3. Copy the caption text from above
4. Repeat for Figure 2

### Markdown:
```markdown
![Figure 1: PDW Simulation Workflow](Figure1_PDW_Workflow.png)
*Figure 1: Complete workflow of the PDW simulation system...*

![Figure 2: Sensor Measurement Error Model](Figure2_Error_Model.png)
*Figure 2: Architecture of the sensor measurement error model...*
```

---

## Technical Specifications

### Figure 1 - PDW Workflow Diagram
- **Resolution:** High (suitable for print)
- **Format:** PNG
- **Color Scheme:** Professional (Blue, Green, Orange, Gray)
- **Content:**
  - 4 distinct phases with color-coded backgrounds
  - Mathematical formulas for parameter calculations
  - Decision diamond for detection logic
  - Clear data flow arrows
  - Legend for notation

### Figure 2 - Error Model Diagram
- **Resolution:** High (suitable for print)
- **Format:** PNG
- **Color Scheme:** Academic (Blue, Green, Orange, Yellow, Gray)
- **Content:**
  - Error model taxonomy
  - Mathematical equations with proper notation
  - Configuration table
  - Gaussian distribution with statistical annotations
  - Detection probability table

---

## Key Points for Report Text

When referencing these figures in your report, consider including:

1. **For Figure 1:**
   - Emphasize the four-phase architecture
   - Highlight vectorized processing for efficiency
   - Explain the probabilistic detection mechanism
   - Detail the mathematical models for each parameter
   - Mention the realistic noise addition in Phase 3

2. **For Figure 2:**
   - Explain the dual-error model (systematic + arbitrary)
   - Justify the choice of Gaussian distribution (Central Limit Theorem)
   - Present the specific error magnitudes and their rationale
   - Discuss the detection probability model
   - Relate error parameters to real-world sensor specifications

---

## References for Report

Suggested references to include when discussing these models:

1. **For Gaussian Noise:**
   - Central Limit Theorem justification
   - Typical radar receiver noise characteristics
   - ADC quantization noise models

2. **For Detection Probability:**
   - Receiver Operating Characteristic (ROC) curves
   - Signal-to-Noise Ratio (SNR) thresholds
   - Probability of detection vs. probability of false alarm

3. **For Path Loss:**
   - Free-space path loss equation
   - Friis transmission equation
   - Radar range equation

---

## Customization Notes

If you need to modify these diagrams:

1. **Change error parameters:** Edit the values in the "Configured Error Parameters" table
2. **Add more radars/sensors:** Update the numbers in Phase 1
3. **Modify detection levels:** Update the "Detection Probability Model" table
4. **Change formulas:** Ensure mathematical notation is consistent

Both diagrams are designed to be:
- ✅ Print-ready (high resolution)
- ✅ Color-blind friendly (distinct colors with patterns)
- ✅ Professionally formatted
- ✅ Mathematically accurate
- ✅ Aligned with your actual implementation

---

**Files Created:**
- `Figure1_PDW_Workflow.png` - Main simulation workflow
- `Figure2_Error_Model.png` - Error model architecture
- `REPORT_FIGURES.md` - This documentation file

**Ready for:** Academic papers, technical reports, presentations, thesis documentation
