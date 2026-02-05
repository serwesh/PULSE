import numpy as np
from pdw_simulator.radar_properties import calculate_doppler_shift, calculate_relative_velocity, apply_doppler_effect
from pdw_simulator.scenario_geometry_functions import get_unit_registry

ureg = get_unit_registry()

def create_error_model(error_config):
    """
    Create an error model based on the configuration.
    
    :param error_config: Dictionary containing error model parameters
    :return: Function that generates errors based on the model
    """
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
        # Parse amplitude
        A, A_unit = parse_value_and_unit(error_config['amplitude'])
        unit = ureg(A_unit)
        
        # Parse frequency
        f, f_unit = parse_value_and_unit(error_config['frequency'])
        if f_unit != 'Hz':
            raise ValueError(f"Frequency unit must be Hz, got {f_unit}")
        
        # Parse phase
        try:
            phi0 = float(error_config['phase'])
        except ValueError:
            raise ValueError(f"Phase must be a numerical value, got {error_config['phase']}")
            
        return lambda t: A * np.sin(2 * np.pi * f * t.magnitude + phi0) * unit
    elif error_config['type'] == 'gaussian':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        unit = ureg(error_unit)
        if error_unit == 'percent':
            # Use Quantity constructor for arrays to be safe or just return dimensionless Quantity
            return lambda size: ureg.Quantity(np.random.normal(0, error_value, size), 'dimensionless')
        else:
            return lambda size: ureg.Quantity(np.random.normal(0, error_value, size), error_unit)
    elif error_config['type'] == 'uniform':
        error_value, error_unit = parse_value_and_unit(error_config['error'])
        unit = ureg(error_unit)
        if error_unit == 'percent':
            return lambda size: ureg.Quantity(np.random.uniform(-error_value, error_value, size), 'dimensionless')
        else:
            return lambda size: ureg.Quantity(np.random.uniform(-error_value, error_value, size), error_unit)
    else:
        raise ValueError(f"Unknown error type: {error_config['type']}")

def parse_value_and_unit(string_value):
    """
    Parse a string containing a value and a unit.
    
    :param string_value: String containing value and unit (e.g., '0.1 dB', '4.5%')
    :return: Tuple of (value, unit)
    """
    parts = string_value.split()
    if len(parts) == 2:
        value, unit = parts
    elif len(parts) == 1:
        value, unit = parts[0], ''
    else:
        raise ValueError(f"Invalid value and unit string: {string_value}")
    
    # Handle percentage
    if value.endswith('%'):
        return float(value[:-1]) / 100, 'percent'
    else:
        return float(value), unit


def detect_pulse(amplitude, detection_levels, detection_probabilities, saturation_level):
    """
    Determine if a pulse is detected based on its amplitude.
    Optimized for performance by using magnitudes.
    """
    # Use magnitudes for fast comparison
    amp_mag = amplitude.magnitude if hasattr(amplitude, 'magnitude') else amplitude
    sat_mag = saturation_level.magnitude if hasattr(saturation_level, 'magnitude') else saturation_level

    if amp_mag > sat_mag:
        return True

    for i in range(len(detection_levels)):
        level = detection_levels[i]
        prob = detection_probabilities[i]
        level_mag = level.magnitude if hasattr(level, 'magnitude') else level

        if amp_mag > level_mag:
            return np.random.random() < prob
    return False

# def detect_pulse(amplitude, detection_levels, detection_probabilities, saturation_level):
#     """
#     Determine if a pulse is detected based on its amplitude.
    
#     :param amplitude: Amplitude of the pulse
#     :param detection_levels: List of detection levels
#     :param detection_probabilities: List of detection probabilities corresponding to levels
#     :param saturation_level: Saturation level of the sensor
#     :return: Boolean indicating whether the pulse is detected
#     """
#     if amplitude.to('dB').magnitude > saturation_level.to('dB').magnitude:
#         return True
    
#     for level, prob in zip(detection_levels,detection_probabilities):
#         if amplitude.to('dB').magnitude > level.to('dB').magnitude:
#             return np.random.random() < prob
#     return False
#         # if amplitude > saturation_level:
#         #     return True
#         # for level, prob in zip(detection_levels, detection_probabilities):
#         #     if amplitude > level:
#         #         return np.random.random() < prob
#         # return False


def measure_amplitude(true_amplitude, r, P_theta, t, P0, amplitude_error_syst, amplitude_error_arb):
    """
    Measure the amplitude of a detected pulse.
    Supports both single values and numpy arrays.
    """
    # Use magnitudes for calculation
    r_mag = r.magnitude if hasattr(r, 'magnitude') else r
    p0_mag = P0.magnitude if hasattr(P0, 'magnitude') else P0
    p_theta_mag = P_theta.magnitude if hasattr(P_theta, 'magnitude') else P_theta
    t_mag = t.magnitude if hasattr(t, 'magnitude') else t
    
    # Path loss (dB)
    pr_mag = 20 * np.log10(r_mag)
    
    # Get systematic and arbitrary errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    
    p_syst = amplitude_error_syst(t)
    p_arb = amplitude_error_arb(size)
    
    p_syst_mag = p_syst.magnitude if hasattr(p_syst, 'magnitude') else p_syst
    p_arb_mag = p_arb.magnitude if hasattr(p_arb, 'magnitude') else p_arb
    
    if size == 1 and isinstance(p_arb_mag, np.ndarray):
        p_arb_mag = p_arb_mag[0]
    
    m_amp_mag = p0_mag - pr_mag + p_theta_mag + p_syst_mag + p_arb_mag
    
    if isinstance(t_mag, np.ndarray) and np.isscalar(m_amp_mag):
        m_amp_mag = np.array([m_amp_mag])
        
    return m_amp_mag * ureg.dBm

# def measure_amplitude(true_amplitude, r, P_theta, t, P0, amplitude_error_syst, amplitude_error_arb):
#     """
#     Measure the amplitude of a detected pulse.
    
#     :param true_amplitude: True amplitude of the pulse (in dB)
#     :param r: Distance between radar and sensor (in meters)
#     :param P_theta: Amplitude correction due to radar antenna lobe pattern (in dB)
#     :param t: Current time
#     :param P0: Amplitude of an emitted pulse from an equivalent omnidirectional radar antenna (in watts)
#     :param amplitude_error_syst: Function to generate systematic error
#     :param amplitude_error_arb: Function to generate arbitrary error
#     :return: Measured amplitude (in dB)
#     """
#     # print("\nDebugging measure_amplitude:")
#     # print(f"true_amplitude: {true_amplitude}, type: {type(true_amplitude)}")
#     # print(f"r: {r}, type: {type(r)}")
#     # print(f"P_theta: {P_theta}, type: {type(P_theta)}")
#     # print(f"t: {t}, type: {type(t)}")
#     # print(f"P0: {P0}, type: {type(P0)}")

#     # Ensure all inputs are Pint Quantities with correct units
#     r = ureg.Quantity(r).to(ureg.meter)
#     P_theta = ureg.Quantity(P_theta).to(ureg.dB)
#     P0 = ureg.Quantity(P0).to(ureg.watt)
    
#     # Convert r to a dimensionless quantity by dividing by 1 meter
#     r_dimensionless = r / ureg.meter
#     Pr = 20 * ureg.dB * np.log10(r_dimensionless.magnitude)
    
#     # Convert P0 from watts to dB
#     P0_dB = 10 * ureg.dB * np.log10(P0.magnitude)
    
#     P_syst = ureg.Quantity(amplitude_error_syst(t)).to(ureg.dB)
#     P_arb = ureg.Quantity(amplitude_error_arb(1)[0]).to(ureg.dB)
    
#     # print(f"After conversion:")
#     # print(f"Pr: {Pr}, Dimensionality: {Pr.dimensionality}")
#     # print(f"P0_dB: {P0_dB}, type: {P0_dB.dimensionality}")
#     # print(f"P_theta: {P_theta}, type: {P_theta.dimensionality}")
#     # print(f"P_syst: {P_syst}, type: {P_syst.dimensionality}")
#     # print(f"P_arb: {P_arb}, type: {P_arb.dimensionality}")


#     # print(f"Pr: {Pr}, Dimensionality: {type(Pr)}")
#     # print(f"P0_dB: {P0_dB}, type: {type(P0_dB)}")
#     # print(f"P_theta: {P_theta}, type: {type(P_theta)}")
#     # print(f"P_syst: {P_syst}, type: {type(P_syst)}")
#     # print(f"P_arb: {P_arb}, type: {type(P_arb)}")
#     total_magnitude = P0_dB.magnitude - Pr.magnitude + P_theta.magnitude + P_syst.magnitude + P_arb.magnitude
#     measured_amplitude = ureg.Quantity(total_magnitude, ureg.dB)
#     # print(f"measured_amplitude: {measured_amplitude}, type: {type(measured_amplitude)}")
    
#     return measured_amplitude


def measure_toa(true_toa, r, t, toa_error_syst, toa_error_arb):
    """
    Measure the Time of Arrival (TOA) of a detected pulse.
    Supports both single values and numpy arrays.
    """
    # Use magnitudes
    true_toa_mag = true_toa.magnitude if hasattr(true_toa, 'magnitude') else true_toa
    r_mag = r.magnitude if hasattr(r, 'magnitude') else r
    t_mag = t.magnitude if hasattr(t, 'magnitude') else t
    
    # Speed of light magnitude
    c_mag = 299792458
    delta_Tr_mag = r_mag / c_mag
    
    # Errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    
    t_syst = toa_error_syst(t)
    t_arb = toa_error_arb(size)
    
    t_syst_mag = t_syst.magnitude if hasattr(t_syst, 'magnitude') else t_syst
    t_arb_mag = t_arb.magnitude if hasattr(t_arb, 'magnitude') else t_arb
    
    if size == 1 and isinstance(t_arb_mag, np.ndarray):
        t_arb_mag = t_arb_mag[0]
    
    # Total TOA magnitude
    m_toa_mag = true_toa_mag + delta_Tr_mag + t_syst_mag + t_arb_mag
    
    if isinstance(t_mag, np.ndarray) and np.isscalar(m_toa_mag):
         m_toa_mag = np.array([m_toa_mag])
         
    return m_toa_mag * ureg.second


def measure_frequency(true_frequency, t, current_time, frequency_error_syst, frequency_error_arb, radar=None, sensor=None):
    """
    Measure frequency with statistical error models and Doppler shift.
    Supports both single values and numpy arrays.
    """
    f_mag = true_frequency.magnitude if hasattr(true_frequency, 'magnitude') else true_frequency
    t_mag = t.magnitude if hasattr(t, 'magnitude') else t
    
    # Apply systematic and arbitrary errors
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    
    f_syst = frequency_error_syst(t)
    f_arb = frequency_error_arb(size)
    
    f_syst_mag = f_syst.magnitude if hasattr(f_syst, 'magnitude') else f_syst
    f_arb_mag = f_arb.magnitude if hasattr(f_arb, 'magnitude') else f_arb
        
    if size == 1 and isinstance(f_arb_mag, np.ndarray):
        f_arb_mag = f_arb_mag[0]
        
    # Standard measurement error
    std_error_mag = np.random.normal(0, 1e6, size) 
    
    measured_freq_mag = f_mag + f_syst_mag + f_arb_mag + std_error_mag
    
    # Apply Doppler shift if radar and sensor are provided
    if radar is not None and sensor is not None:
        # Doppler usually returns a Quantity. If we have arrays, it might be tricky.
        # But apply_doppler_effect usually handles Quantities.
        measured_freq = apply_doppler_effect(measured_freq_mag * ureg.Hz, radar, sensor)
        return abs(measured_freq)
    
    if isinstance(t_mag, np.ndarray) and np.isscalar(measured_freq_mag):
         measured_freq_mag = np.array([measured_freq_mag])
    
    return abs(measured_freq_mag) * ureg.Hz


def measure_pulse_width(true_pw, t, pw_error_syst, pw_error_arb):
    """
    Measure the pulse width of a detected pulse.
    Supports both single values and numpy arrays.
    """
    pw_mag = true_pw.magnitude if hasattr(true_pw, 'magnitude') else true_pw
    t_mag = t.magnitude if hasattr(t, 'magnitude') else t
    
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    
    pw_syst = pw_error_syst(t)
    pw_arb = pw_error_arb(size)

    pw_syst_mag = pw_syst.magnitude if hasattr(pw_syst, 'magnitude') else pw_syst
    pw_arb_mag = pw_arb.magnitude if hasattr(pw_arb, 'magnitude') else pw_arb
    
    if size == 1 and isinstance(pw_arb_mag, np.ndarray):
        pw_arb_mag = pw_arb_mag[0]
        
    # Handling percent or dimensionless arbitrary error
    if hasattr(pw_arb, 'units') and pw_arb.units == ureg.percent:
        pw_arb_mag = pw_mag * pw_arb_mag / 100
    elif hasattr(pw_arb, 'dimensionless') and pw_arb.dimensionless:
        pw_arb_mag = pw_mag * pw_arb_mag

    m_pw_mag = pw_mag + pw_syst_mag + pw_arb_mag
    
    if isinstance(t_mag, np.ndarray) and np.isscalar(m_pw_mag):
         m_pw_mag = np.array([m_pw_mag])
         
    return m_pw_mag * ureg.second


def measure_aoa(true_aoa, t, aoa_error_syst, aoa_error_arb):
    """
    Measure the Angle of Arrival (AOA) of a detected pulse.
    Supports both single values and numpy arrays.
    """
    aoa_mag = true_aoa.magnitude if hasattr(true_aoa, 'magnitude') else true_aoa
    t_mag = t.magnitude if hasattr(t, 'magnitude') else t
    
    size = len(t_mag) if isinstance(t_mag, np.ndarray) else 1
    
    a_syst = aoa_error_syst(t)
    a_arb = aoa_error_arb(size)
    
    a_syst_mag = a_syst.magnitude if hasattr(a_syst, 'magnitude') else a_syst
    a_arb_mag = a_arb.magnitude if hasattr(a_arb, 'magnitude') else a_arb
    
    if size == 1 and isinstance(a_arb_mag, np.ndarray):
        a_arb_mag = a_arb_mag[0]
    
    m_aoa_mag = aoa_mag + a_syst_mag + a_arb_mag
    
    if isinstance(t_mag, np.ndarray) and np.isscalar(m_aoa_mag):
         m_aoa_mag = np.array([m_aoa_mag])
         
    return m_aoa_mag * ureg.degree

# Additional function for AOA sinusoidal error
def aoa_sinusoidal_error(AOA, A, f, AOA_ref):
    """
    Calculate AOA error with sinusoidal dependency on the direction.
    
    :param AOA: Angle of Arrival
    :param A: Error amplitude
    :param f: Number of sinus periods per 360 degrees
    :param AOA_ref: Reference angle where error is zero
    :return: AOA error
    """
    return A * np.sin(f * (AOA - AOA_ref))