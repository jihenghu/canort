"""
Example script demonstrating the usage of sensor configurations in CanORT.
This script shows how to create and use different sensor configurations.
"""

import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.io.sensor_list import amsre, smap, smos, gmi, ssmis, amsr2, mwri

def main():
    # Example 1: Create a SMAP sensor with default settings
    smap_sensor = smap()
    print("\n1. SMAP sensor with default settings:")
    print(smap_sensor)
    
    # Example 2: Create an AMSR2 sensor with custom frequency
    amsr2_sensor = amsr2(frequency=10.65)
    print("\n2. AMSR2 sensor with 10.65 GHz:")
    print(amsr2_sensor)
    
    # Example 3: Create a GMI sensor with custom viewing angle
    gmi_sensor = gmi(theta=45.0)
    print("\n3. GMI sensor with 45° viewing angle:")
    print(gmi_sensor)
    
    # Example 4: Create a SMOS sensor with only vertical polarization
    smos_sensor = smos(polarization=["V"])
    print("\n4. SMOS sensor with vertical polarization only:")
    print(smos_sensor)
    
    # Example 5: Create a MWRI sensor with multiple frequencies
    mwri_sensor = mwri(frequency=[10.65, 18.7, 23.8])
    print("\n5. MWRI sensor with selected frequencies:")
    print(mwri_sensor)
    
    # Example 6: Create an SSMIS sensor with all parameters customized
    ssmis_sensor = ssmis(
        frequency=37.0,
        theta=50.0,
        polarization=["H", "V"]
    )
    print("\n6. SSMIS sensor with all parameters customized:")
    print(ssmis_sensor)
    
    # Example 7: Create an AMSR-E sensor with multiple frequencies and custom angle
    amsre_sensor = amsre(
        frequency=[6.925, 10.65, 18.7],
        theta=52.0
    )
    print("\n7. AMSR-E sensor with multiple frequencies and custom angle:")
    print(amsre_sensor)
    
    # Example 8: Demonstrate wavelength calculation
    print("\n8. Wavelength calculation for SMAP sensor:")
    print(f"Frequency: {smap_sensor.frequency} GHz")
    print(f"Wavelength: {smap_sensor.wavelength:.3f} m")
    print(f"Wave number: {smap_sensor.wavenumber:.3f} m⁻¹")

if __name__ == "__main__":
    main() 