import pytest
import numpy as np
from pdw_simulator.models import Radar
from pdw_simulator.scenario_geometry_functions import get_unit_registry

ureg = get_unit_registry()

def test_radar_pri_calculation():
    config = {
        'name': 'TestRadar',
        'start_position': [0, 0],
        'rotation_type': 'constant',
        'rotation_params': {'t0': 0, 'alpha0': 0, 'T_rot': 4},
        'pri_type': 'fixed',
        'pri_params': {'pri': 0.001},
        'frequency_type': 'fixed',
        'frequency_params': {'frequency': 1e9},
        'pulse_width_type': 'fixed',
        'pulse_width_params': {'pulse_width': 1e-6},
         'lobe_pattern': {
            'type': 'Sinc',
            'main_lobe_opening_angle': 0,
            'radar_power_at_main_lobe': 0,
            'radar_power_at_back_lobe': -30
        },
        'power': 100
    }
    
    radar = Radar(config)
    end_time = 0.01 * ureg.second
    # Manually trigger pulse time calculation
    radar.calculate_pulse_times(end_time)
    
    # Test first pulse (should be 0)
    pri0 = radar.get_pri_for_pulse(0.0)
    assert pri0.magnitude == 0.0
    
    # Test second pulse (should be PRI)
    pri1 = radar.get_pri_for_pulse(0.001)
    assert np.isclose(pri1.magnitude, 0.001)
    
    # Test arbitrary time (should be 0 because not a pulse time)
    pri_invalid = radar.get_pri_for_pulse(0.0005)
    assert pri_invalid.magnitude == 0.0

if __name__ == "__main__":
    test_radar_pri_calculation()
