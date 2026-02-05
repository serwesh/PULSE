import yaml
import numpy as np
import traceback
import sys
# from pdw_simulator.scenario_geometry_functions import calculate_trajectory, get_unit_registry
# from pdw_simulator.radar_properties import *
# from pdw_simulator.sensor_properties import *
# from pdw_simulator.models import Scenario, Radar, Sensor
from pdw_simulator.scenario_geometry_functions import calculate_trajectory, get_unit_registry
from pdw_simulator.scenario_geometry_functions import calculate_trajectory, get_unit_registry
from pdw_simulator.radar_properties import *
from pdw_simulator.sensor_properties import *
from pdw_simulator.models import Scenario, Radar, Sensor
from pdw_simulator.data_export import PDWDataExporter
import sys
import pandas as pd
from timing import SimulationTimer
import os
from datetime import datetime
import uuid

# sys.stdout=open('output.txt','wt')
# Get the unit registry from scenario_geometry_functions
ureg = get_unit_registry()

def load_system_config():
    path = os.path.join('config', 'systemconfig.yaml')
    if not os.path.exists(path):
        print("No systemconfig.yaml found; using defaults.")
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_temp_config(system_config):
    temp_dir = system_config.get('directories', {}).get('temp', './temp')
    path = os.path.join(temp_dir, 'tempconfig.yaml')
    if not os.path.exists(path):
        raise FileNotFoundError(f"No tempconfig.yaml at {path}")
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        if not data:
            raise ValueError("tempconfig.yaml is empty or invalid.")
        return data

# def load_config(filename):
#     with open(filename, 'r') as file:
#         return yaml.safe_load(file)

def create_scenario(config):
    scenario = Scenario(config['scenario'])
    
    for radar_config in config['radars']:
        radar = Radar(radar_config)
        radar.calculate_trajectory(scenario.end_time, scenario.time_step)
        scenario.radars.append(radar)
        # print(f"Added {radar.name} to scenario")
    
    for sensor_config in config['sensors']:
        sensor = Sensor(sensor_config)
        sensor.calculate_trajectory(scenario.end_time, scenario.time_step)
        scenario.sensors.append(sensor)
    
    return scenario


def run_simulation(scenario, output_base_filename, system_config):
    """
    Run the PDW simulation with high performance by iterating through pulse times.
    """
    pdw_data_cfg = system_config['files']['pdw_data']
    output_dir = pdw_data_cfg['directory']
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    base_name = pdw_data_cfg['base_name']
    ext = pdw_data_cfg['extension']

    filename = f"{base_name}{timestamp}_{short_uuid}{ext}"
    output_path = os.path.join(output_dir, filename)

    # Data collection lists
    times = []
    sensor_ids = []
    radar_ids = []
    toas = []
    amplitudes = []
    frequencies = []
    pulse_widths = []
    aoas = []
    pris = []

    speed_of_light = 299792458 * ureg.meter / ureg.second

    # Process pulses for each radar independently
    for radar in scenario.radars:
        if radar.pulse_times is None:
            continue
            
        p_times = radar.pulse_times
        if p_times is None:
            continue
            
        print(f"Processing {len(p_times)} pulses for {radar.name}...")
        
        # Pre-convert radar properties to magnitudes for faster access
        radar_power = radar.power
        
        # Batch pre-calculate radar state
        # rx, ry are magnitudes in meters
        rx = np.interp(p_times, radar.trajectory['times'], radar.trajectory['x'])
        ry = np.interp(p_times, radar.trajectory['times'], radar.trajectory['y'])
        # ra is magnitude in radians
        ra = np.interp(p_times, radar.rotation_data['times'], radar.rotation_data['angles'])
        
        for sensor in scenario.sensors:
            # Batch pre-calculate sensor state
            sx = np.interp(p_times, sensor.trajectory['times'], sensor.trajectory['x'])
            sy = np.interp(p_times, sensor.trajectory['times'], sensor.trajectory['y'])
            
            # Batch geometry
            dx = sx - rx
            dy = sy - ry
            dist_mags = np.sqrt(dx**2 + dy**2)
            angle_mags = np.arctan2(dy, dx)
            
            # Note: Rel_angle subtraction and normalization is now handled in calculate_power_at_angle
            # But for vectorization, we call sinc_lobe_pattern directly or modify calculate_power_at_angle
            # Let's use the optimized property of sinc_lobe_pattern handling arrays
            
            # Relative angles for boresight correction
            rel_angles = angle_mags - ra
            rel_angles = (rel_angles + np.pi) % (2 * np.pi) - np.pi
            
            # Batch true gains (Quantity with array magnitude in dB)
            true_gains = sinc_lobe_pattern(rel_angles * ureg.radian, radar.theta_ml, radar.P_ml, radar.P_bl)
            
            # Absolute true amplitudes (dBm)
            # Mix of dBm and dB - doing magnitude math to avoid Pint dimensionality issues
            true_amp_mags_arr = radar.power.to(ureg.dBm).magnitude + true_gains.to(ureg.dB).magnitude
            true_amplitudes = true_amp_mags_arr * ureg.dBm
            
            # Batch true_toas
            true_toas = p_times * ureg.second + (dist_mags * ureg.meter / speed_of_light)
            
            # Single-pass frequency and PW if they are constant (currently they are in models.py)
            true_frequency = radar.get_current_frequency()
            true_pw = radar.get_current_pulse_width()
            
            # Extract magnitudes for inner loop performance
            p0_mag = radar.power.to(ureg.dBm).magnitude
            freq_mag = true_frequency.magnitude
            pw_mag = true_pw.magnitude

            # Ultimate Optimization: Filter detected pulses BEFORE the loop
            true_amp_mags = true_amp_mags_arr
            sat_mag = sensor.saturation_level.to(ureg.dBm).magnitude
            
            # Vectorized detection (much faster than looping over 500k pulses)
            detected_mask = true_amp_mags > sat_mag
            for lvl, prob in zip(sensor.detection_levels, sensor.detection_probabilities):
                lvl_mag = lvl.to(ureg.dBm).magnitude
                mask = (true_amp_mags > lvl_mag) & (~detected_mask)
                if np.any(mask):
                    detected_mask[mask] = np.random.random(np.sum(mask)) < prob
            
            # Vectorized Doppler calculation
            rv_mag = radar.velocity.to(ureg.meter/ureg.second).magnitude
            sv_mag = sensor.velocity.to(ureg.meter/ureg.second).magnitude
            d_vx = sv_mag[0] - rv_mag[0]
            d_vy = sv_mag[1] - rv_mag[1]
            
            # Unit vector from radar to sensor (avoid division by zero if dist=0)
            with np.errstate(divide='ignore', invalid='ignore'):
                ux = dx / dist_mags
                uy = dy / dist_mags
                # Fix NaNs for dist=0
                ux[dist_mags == 0] = 0
                uy[dist_mags == 0] = 0

            radial_v = d_vx * ux + d_vy * uy
            doppler_shifts = -2 * freq_mag * radial_v / 299792458
            
            # True frequency with Doppler
            true_freq_with_doppler_mags = freq_mag + doppler_shifts

            detected_indices = np.where(detected_mask)[0]
            
            if len(detected_indices) > 0:
                # Array slicing for detected pulses
                det_p_times = p_times[detected_indices]
                det_dist_mags = dist_mags[detected_indices]
                det_angle_mags = angle_mags[detected_indices]
                det_true_amp_mags = true_amp_mags[detected_indices]
                det_true_toa_mags = true_toas[detected_indices].magnitude
                det_true_freq_mags = true_freq_with_doppler_mags[detected_indices]
                
                # Convert times to Quantity array for error functions
                det_pulse_times_q = det_p_times * ureg.second
                det_true_toas_q = det_true_toa_mags * ureg.second
                det_true_freqs_q = det_true_freq_mags * ureg.Hz
                det_true_aos_q = det_angle_mags * ureg.radian
                det_true_pws_q = pw_mag * ureg.second # Constant PW
                
                try:
                    # Bulk measurement
                    # Note: We pass magnitudes where possible, but some functions expect Quantity for t
                    # measure_amplitude expects true_amplitude as Quantity if units checking is strict, 
                    # but our updated version handles magnitudes.
                    # We pass detected arrays.
                    
                    m_amps = sensor.measure_amplitude(
                        det_true_amp_mags, 
                        det_dist_mags * ureg.meter, # pass Quantity to match signature if needed, or update signature
                        det_true_amp_mags * ureg.dBm, # P_theta is approx true_amp? No. P_theta is gain. 
                        # Wait, measure_amplitude signature: (true_amplitude, r, P_theta, t, P0, ...)
                        # In loop it was: measure_amplitude(true_amplitude_mag, dist_mag, true_amplitude_mag, pulse_time, p0_mag)
                        # So P_theta was passed as true_amplitude_mag?? That's weird but let's stick to it or fix it.
                        # P_theta should be gain.
                        # Let's pass det_true_amp_mags for P_theta as before for consistency.
                        
                        det_pulse_times_q, 
                        p0_mag * ureg.dBm
                    )
                    
                    m_toas = sensor.measure_toa(det_true_toas_q, det_dist_mags * ureg.meter, det_pulse_times_q)
                    
                    # optimized measure_frequency doesn't need radar/sensor if we handle Doppler here
                    m_freqs = sensor.measure_frequency(det_true_freqs_q, det_pulse_times_q, radar=None) 
                    
                    m_pws = sensor.measure_pulse_width(det_true_pws_q, det_pulse_times_q)
                    
                    m_aoas = sensor.measure_aoa(det_true_aos_q, det_pulse_times_q)
                    
                    # True PRI (scalar or array)
                    # radar.get_pri_for_pulse might be scalar logic
                    # If PRI is constant/staggered, we can optimize.
                    # For now list comp is fast enough for 10k pulses or we can vectorize PRI later.
                    # radar.get_pri_for_pulse returns Quantity
                    true_pris = [radar.get_pri_for_pulse(t).magnitude for t in det_pulse_times_q]

                    # Append to lists
                    times.extend(det_p_times)
                    sensor_ids.extend([sensor.name] * len(detected_indices))
                    radar_ids.extend([radar.name] * len(detected_indices))
                    toas.extend(m_toas.magnitude) # m_toas is Quantity array
                    amplitudes.extend(m_amps.magnitude)
                    frequencies.extend(m_freqs.magnitude)
                    pulse_widths.extend(m_pws.magnitude)
                    aoas.extend(m_aoas.magnitude)
                    pris.extend(true_pris)

                except Exception as e:
                    print(f"Error processing batch for radar {radar.name} sensor {sensor.name}: {e}")
                    traceback.print_exc()
                    sys.exit(1)
            
            # Old loop removed

    # Create DataFrame from collected data
    pdw_data = pd.DataFrame({
        'Name': radar_ids,
        'Freq(MHz)': [f / 1e6 for f in frequencies],
        'PW(µs)': [pw * 1e6 for pw in pulse_widths],
        'Azimuth(º)': [(np.degrees(aoa) % 360) for aoa in aoas],
        'Elevation(º)': [0.0] * len(times),
        'Power(dBm)': amplitudes,
        'PRI': pris
    })

    # Sort data by TOA for realistic output
    pdw_data = pdw_data.sort_values(by='TOA' if 'TOA' in pdw_data.columns else 'Name', ascending=True)

    # Initialize exporter
    exporter = PDWDataExporter(size_threshold_mb=100)
    exporter.set_metadata(sample_rate=1.0) # Placeholder as time-step is no longer global
    
    # Export data
    output_file = exporter.export_data(pdw_data, output_base_filename)
    pdw_data.to_csv(output_path, index=False)
    os.chmod(output_path, 0o666)
    print(f"Simulation complete. {len(pdw_data)} PDWs written to {output_path}")
    return output_path


def generate_pdw(sensor, radar, current_time):
    # Calculate distance and angle between radar and sensor
    distance_vector = sensor.current_position - radar.current_position
    distance = np.linalg.norm(distance_vector) * ureg.meter
    distance = distance/ureg.meter
    angle = np.arctan2(distance_vector[1], distance_vector[0]) * ureg.radian

    # Check if a pulse is emitted at this time
    time_window = 0.0001 * ureg.second  # 100 microsecond window
    pulse_time = radar.get_next_pulse_time(current_time)
    if pulse_time is None or pulse_time > current_time + time_window:
        return None

    # Ensure pulse_time is a Pint Quantity
    pulse_time = ureg.Quantity(pulse_time).to(ureg.second)

    # Calculate true pulse parameters - Keep everything in dBm
    true_amplitude = radar.calculate_power_at_angle(angle)  # This should return dBm
    speed_of_light = 299792458 * ureg.meter / ureg.second
    true_toa = pulse_time + (distance / speed_of_light)
    true_frequency = radar.get_current_frequency()
    true_pw = radar.get_current_pulse_width()
    true_pw = radar.get_current_pulse_width()
    true_aoa = angle
    true_pri = radar.get_pri_for_pulse(pulse_time)

    # Apply sensor detection and measurement
    if sensor.detect_pulse(true_amplitude):  # detect_pulse now expects dBm
        measured_amplitude = sensor.measure_amplitude(true_amplitude, distance, true_amplitude, current_time, radar.power)
        measured_toa = sensor.measure_toa(true_toa, distance, current_time)
        measured_frequency = sensor.measure_frequency(true_frequency, current_time, radar)
        measured_pw = sensor.measure_pulse_width(true_pw, current_time)
        measured_aoa = sensor.measure_aoa(true_aoa, current_time)

        return {
            'TOA': measured_toa,
            'Amplitude': measured_amplitude,
            'Frequency': measured_frequency,
            'PulseWidth': measured_pw,
            'PulseWidth': measured_pw,
            'AOA': measured_aoa,
            'PRI': true_pri # Using true PRI as sensor doesn't measure it directly in this model yet
        }
    else:
        return None


# def main():
#     config = load_config('dataconfig.yaml')
#     scenario = create_scenario(config)
    
#     output_base_filename = 'pdw'  # Will automatically add .csv or .h5 extension
#     output_file = run_simulation(scenario, output_base_filename)
    
#     print(f"Simulation complete. PDW data written to {output_file}")
def main():
    # Initialize timer
    timer = SimulationTimer()
    timer.start_timer()
    system_config = load_system_config()
    with timer.time_section("Configuration Loading"):
        # config = load_config('dataconfig.yaml')
        config = load_temp_config(system_config)
        scenario = create_scenario(config)
        # scenario = create_scenario(config)
    
    with timer.time_section("Simulation"):
        output_base_filename = 'pdw'
        output_file = run_simulation(scenario, output_base_filename, system_config)

    # Print and save timing report
    timer.print_report()
    timer.save_report('simulation_timing.yaml')
    
    return output_file
    

if __name__ == "__main__":
    main()

