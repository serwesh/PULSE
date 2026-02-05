# 🎯 Quick Reference: Where Noise is Added in the Code

## 📍 Location Map

### Main Files for Noise Addition:
1. **`src/pdw_simulator/sensor_properties.py`** - All measurement functions
2. **`dataconfig.yaml`** - Error configuration parameters

---

## 🔊 Amplitude Noise

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `measure_amplitude()` (lines 126-157)

```python
def measure_amplitude(true_amplitude, r, P_theta, t, P0, 
                     amplitude_error_syst, amplitude_error_arb):
    # Extract magnitudes
    r_mag = r.magnitude if hasattr(r, 'magnitude') else r
    p0_mag = P0.magnitude if hasattr(P0, 'magnitude') else P0
    
    # Calculate path loss
    pr_mag = 20 * np.log10(r_mag)
    
    # Get errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    p_syst = amplitude_error_syst(t)      # ← SYSTEMATIC ERROR
    p_arb = amplitude_error_arb(size)     # ← ARBITRARY ERROR
    
    # Add noise to measurement
    m_amp_mag = p0_mag - pr_mag + p_theta_mag + p_syst_mag + p_arb_mag
    
    return m_amp_mag * ureg.dBm
```

**Configuration in `dataconfig.yaml`:**
```yaml
amplitude_error:
  systematic:
    type: "constant"
    error: "0 dBm"        # No systematic bias
  arbitrary:
    type: "gaussian"
    error: "2 dBm"        # ±2 dBm random noise
```

**What it does:**
- Adds ±2 dBm Gaussian noise to every amplitude measurement
- 68% of measurements within ±2 dBm of true value

---

## ⏱️ Time of Arrival (TOA) Noise

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `measure_toa()` (lines 214-246)

```python
def measure_toa(true_toa, r, t, toa_error_syst, toa_error_arb):
    # Get magnitudes
    true_toa_mag = true_toa.magnitude
    r_mag = r.magnitude
    
    # Calculate propagation delay
    c_mag = 299792458  # Speed of light
    delta_Tr_mag = r_mag / c_mag
    
    # Get errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    t_syst = toa_error_syst(t)      # ← SYSTEMATIC ERROR
    t_arb = toa_error_arb(size)     # ← ARBITRARY ERROR
    
    # Add noise to measurement
    m_toa_mag = true_toa_mag + delta_Tr_mag + t_syst_mag + t_arb_mag
    
    return m_toa_mag * ureg.second
```

**Configuration in `dataconfig.yaml`:**
```yaml
toa_error:
  systematic:
    type: "constant"
    error: "0 s"          # No systematic bias
  arbitrary:
    type: "gaussian"
    error: "5e-9 s"       # ±5 nanoseconds random noise
```

**What it does:**
- Adds ±5 nanosecond Gaussian noise to TOA
- Very precise timing!

---

## 📻 Frequency Noise

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `measure_frequency()` (lines 249-284)

```python
def measure_frequency(true_frequency, t, current_time, 
                     frequency_error_syst, frequency_error_arb, 
                     radar=None, sensor=None):
    # Get magnitude
    f_mag = true_frequency.magnitude
    
    # Get errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    f_syst = frequency_error_syst(t)      # ← SYSTEMATIC ERROR
    f_arb = frequency_error_arb(size)     # ← ARBITRARY ERROR
    
    # Standard measurement error
    std_error_mag = np.random.normal(0, 1e6, size)  # ±1 MHz
    
    # Add all noise sources
    measured_freq_mag = f_mag + f_syst_mag + f_arb_mag + std_error_mag
    
    return abs(measured_freq_mag) * ureg.Hz
```

**Configuration in `dataconfig.yaml`:**
```yaml
frequency_error:
  systematic:
    type: "constant"
    error: "0 Hz"         # No systematic bias
  arbitrary:
    type: "gaussian"
    error: "1%"           # 1% of frequency as noise
```

**What it does:**
- Adds 1% Gaussian noise (for 1.5 GHz = ±15 MHz)
- Plus additional ±1 MHz standard error
- Total: ~±16 MHz variation

---

## ⏲️ Pulse Width Noise

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `measure_pulse_width()` (lines 287-317)

```python
def measure_pulse_width(true_pw, t, pw_error_syst, pw_error_arb):
    # Get magnitude
    pw_mag = true_pw.magnitude
    
    # Get errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    pw_syst = pw_error_syst(t)      # ← SYSTEMATIC ERROR
    pw_arb = pw_error_arb(size)     # ← ARBITRARY ERROR
    
    # Handle percentage errors
    if hasattr(pw_arb, 'units') and pw_arb.units == ureg.percent:
        pw_arb_mag = pw_mag * pw_arb_mag / 100
    
    # Add noise to measurement
    m_pw_mag = pw_mag + pw_syst_mag + pw_arb_mag
    
    return m_pw_mag * ureg.second
```

**Configuration in `dataconfig.yaml`:**
```yaml
pulse_width_error:
  systematic:
    type: "constant"
    error: "0 s"          # No systematic bias
  arbitrary:
    type: "gaussian"
    error: "25e-9 s"      # ±25 nanoseconds random noise
```

**What it does:**
- Adds ±25 nanosecond Gaussian noise
- For 100 µs pulse: 0.025% error

---

## 🧭 Angle of Arrival (AOA) Noise

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `measure_aoa()` (lines 320-344)

```python
def measure_aoa(true_aoa, t, aoa_error_syst, aoa_error_arb):
    # Get magnitude
    aoa_mag = true_aoa.magnitude
    
    # Get errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    a_syst = aoa_error_syst(t)      # ← SYSTEMATIC ERROR
    a_arb = aoa_error_arb(size)     # ← ARBITRARY ERROR
    
    # Add noise to measurement
    m_aoa_mag = aoa_mag + a_syst_mag + a_arb_mag
    
    return m_aoa_mag * ureg.degree
```

**Configuration in `dataconfig.yaml`:**
```yaml
aoa_error:
  systematic:
    type: "constant"
    error: "0 deg"        # No systematic bias
  arbitrary:
    type: "gaussian"
    error: "3.5 deg"      # ±3.5 degrees random noise
```

**What it does:**
- Adds ±3.5° Gaussian noise to angle measurements
- Simulates antenna direction-finding accuracy

---

## 🎲 Error Model Creation

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `create_error_model()` (lines 7-56)

This function converts YAML configuration into executable error functions:

```python
def create_error_model(error_config):
    if error_config['type'] == 'constant':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        unit = ureg(error_unit)
        return lambda t: error_value * unit
    
    elif error_config['type'] == 'linear':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        rate_value, rate_unit = parse_value_and_unit(error_config['rate'])
        unit = ureg(error_unit)
        return lambda t: (error_value + rate_value * t.magnitude) * unit
    
    elif error_config['type'] == 'sinus':
        A, A_unit = parse_value_and_unit(error_config['amplitude'])
        f, f_unit = parse_value_and_unit(error_config['frequency'])
        phi0 = float(error_config['phase'])
        unit = ureg(A_unit)
        return lambda t: A * np.sin(2 * np.pi * f * t.magnitude + phi0) * unit
    
    elif error_config['type'] == 'gaussian':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        if error_unit == 'percent':
            return lambda size: ureg.Quantity(
                np.random.normal(0, error_value, size), 'dimensionless')
        else:
            return lambda size: ureg.Quantity(
                np.random.normal(0, error_value, size), error_unit)
    
    elif error_config['type'] == 'uniform':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        if error_unit == 'percent':
            return lambda size: ureg.Quantity(
                np.random.uniform(-error_value, error_value, size), 
                'dimensionless')
        else:
            return lambda size: ureg.Quantity(
                np.random.uniform(-error_value, error_value, size), 
                error_unit)
```

---

## 🎯 Detection Probability (Another Form of "Noise")

**File:** `src/pdw_simulator/sensor_properties.py`  
**Function:** `detect_pulse()` (lines 80-99)

```python
def detect_pulse(amplitude, detection_levels, detection_probabilities, 
                saturation_level):
    # Use magnitudes for fast comparison
    amp_mag = amplitude.magnitude
    sat_mag = saturation_level.magnitude
    
    # Always detect if above saturation
    if amp_mag > sat_mag:
        return True
    
    # Probabilistic detection based on levels
    for i in range(len(detection_levels)):
        level = detection_levels[i]
        prob = detection_probabilities[i]
        level_mag = level.magnitude
        
        if amp_mag > level_mag:
            return np.random.random() < prob  # ← RANDOM DETECTION
    
    return False  # Not detected
```

**Configuration in `dataconfig.yaml`:**
```yaml
saturation_level: "-65 dBm"
detection_probability:
  level: [-65, -70, -75, -80]      # dBm
  probability: [100, 90, 70, 50]   # percent
```

**What it does:**
- Signals above -65 dBm: 100% detection
- Signals -65 to -70 dBm: 100% detection
- Signals -70 to -75 dBm: 90% detection
- Signals -75 to -80 dBm: 70% detection
- Signals below -80 dBm: 50% detection

---

## 📊 How to Change Noise Levels

### Make Sensor More Accurate:
```yaml
amplitude_error:
  arbitrary:
    error: "0.5 dBm"  # Changed from "2 dBm"
```

### Make Sensor Less Accurate:
```yaml
amplitude_error:
  arbitrary:
    error: "5 dBm"    # Changed from "2 dBm"
```

### Add Systematic Drift:
```yaml
amplitude_error:
  systematic:
    type: "linear"
    error: "0 dBm"
    rate: "0.1 dBm/s"  # Drift over time
```

### Add Periodic Interference:
```yaml
amplitude_error:
  systematic:
    type: "sinus"
    amplitude: "1 dBm"
    frequency: "5 Hz"
    phase: 0
```

---

## 🔍 Tracing a Single Pulse Through the Code

Let's trace what happens to **one pulse** from Radar1:

### Step 1: Pulse Emission
**File:** `src/pdw_simulator/main.py`, line 100
```python
p_times = radar.pulse_times  # [0.0, 0.0006, 0.0012, ...]
```

### Step 2: Calculate True Values
**File:** `src/pdw_simulator/main.py`, lines 111-148
```python
# Position
rx = 100 meters, ry = 200 meters
sx = 2000 meters, sy = 2000 meters

# Distance
distance = sqrt((2000-100)² + (2000-200)²) = 2,613 meters

# Angle
angle = arctan2(1800, 1900) = 0.758 radians = 43.4°

# Amplitude
gain = sinc_lobe_pattern(angle - boresight)
true_amplitude = 40 dBm + gain - path_loss
```

### Step 3: Detection Check
**File:** `src/pdw_simulator/main.py`, lines 160-165
```python
detected_mask = true_amp_mags > sat_mag
# If true_amplitude = -68 dBm:
# -68 > -70? Yes → Check 90% probability
# random() = 0.35 < 0.90? Yes → DETECTED!
```

### Step 4: Add Noise
**File:** `src/pdw_simulator/main.py`, lines 212-233
```python
# Amplitude
m_amps = sensor.measure_amplitude(...)
# Inside: adds +1.2 dBm random noise
# Result: -68 + 1.2 = -66.8 dBm

# TOA
m_toas = sensor.measure_toa(...)
# Inside: adds +2.3e-9 s random noise
# Result: 1.500008716 + 0.0000000023 = 1.500008718 s

# Frequency
m_freqs = sensor.measure_frequency(...)
# Inside: adds +8.5 MHz random noise
# Result: 1500 MHz + 8.5 = 1508.5 MHz

# Pulse Width
m_pws = sensor.measure_pulse_width(...)
# Inside: adds +18 ns random noise
# Result: 100,000 ns + 18 = 100,018 ns

# AOA
m_aoas = sensor.measure_aoa(...)
# Inside: adds +2.3° random noise
# Result: 43.4° + 2.3 = 45.7°
```

### Step 5: Save to Output
**File:** `src/pdw_simulator/main.py`, lines 243-251
```python
times.extend([0.0])
radar_ids.extend(['Radar1'])
amplitudes.extend([-66.8])
frequencies.extend([1508.5e6])
pulse_widths.extend([100.018e-6])
aoas.extend([45.7])
```

### Step 6: Export to CSV
**File:** `src/pdw_simulator/main.py`, lines 261-280
```csv
Name,Freq(MHz),PW(µs),Azimuth(º),Elevation(º),Power(dBm),PRI
Radar1,1508.5,100.018,45.7,0.0,-66.8,0.0006
```

---

## 💡 Key Insights

1. **Every measurement goes through the same pattern:**
   ```
   True Value → Systematic Error → Arbitrary Error → Measured Value
   ```

2. **Noise is added in `sensor_properties.py`:**
   - Each `measure_*()` function adds noise
   - Error models are created from YAML config

3. **Two independent noise sources:**
   - Systematic: Same for all measurements (bias)
   - Arbitrary: Different for each measurement (random)

4. **Detection is also probabilistic:**
   - Weak signals might be missed
   - This is another form of "noise" (missing data)

5. **Configuration is king:**
   - All noise parameters in `dataconfig.yaml`
   - Easy to adjust without changing code

---

## 🎓 Learning Exercise

Try this to understand better:

1. **Run simulation with current settings**
   ```bash
   python src/pdw_simulator/main.py
   ```

2. **Change amplitude error to 0:**
   ```yaml
   amplitude_error:
     arbitrary:
       error: "0 dBm"
   ```

3. **Run again and compare outputs**
   - You'll see amplitude values are now "perfect"
   - Other parameters still have noise

4. **Gradually increase noise:**
   ```yaml
   error: "0.5 dBm"  # Small noise
   error: "2 dBm"    # Medium noise
   error: "10 dBm"   # Large noise
   ```

5. **Observe how data quality degrades**

---

**Happy Coding! 🚀**
