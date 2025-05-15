"""
Example script demonstrating the usage of soil creation functions in CanORT.
This script shows how to create different types of soil instances.
"""

import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.io.make_soil import (
    make_soil,
    create_sandy_soil,
    create_clayey_soil,
    create_loamy_soil
)
from src.io.sensor_list import smap

def main():
    # Example 1: Create a basic soil with default parameters
    soil1 = make_soil()
    print("\n1. Basic soil with default parameters:")
    print(soil1)
    
    # Example 2: Create a sandy soil
    soil2 = create_sandy_soil()
    print("\n2. Sandy soil (80% sand, 10% clay):")
    print(soil2)
    
    # Example 3: Create a clayey soil
    soil3 = create_clayey_soil()
    print("\n3. Clayey soil (20% sand, 60% clay):")
    print(soil3)
    
    # Example 4: Create a loamy soil
    soil4 = create_loamy_soil()
    print("\n4. Loamy soil (40% sand, 20% clay):")
    print(soil4)
    
    # Example 5: Create a soil with custom parameters
    soil5 = make_soil(
        temperature=298.15,  # 25°C
        moisture=0.3,  # 30% moisture
        sand=0.6,
        clay=0.2,
        rms_hgt=0.01,  # 1 cm
        corr_length=0.05,  # 5 cm
        diel_model="mironov"
    )
    print("\n5. Custom soil with all parameters specified:")
    print(soil5)
    
    # Example 6: Calculate dielectric constant for different soil types
    sensor = smap()  # Use SMAP sensor configuration
    print(sensor)

    print("\n6. Dielectric constant calculation for different soil types:")
    print(f"Sandy soil: {soil2.dielectric_constant(sensor):.3f}")
    print(f"Clayey soil: {soil3.dielectric_constant(sensor):.3f}")
    print(f"Loamy soil: {soil4.dielectric_constant(sensor):.3f}")
    
    # Example 7: Create soils with different dielectric models
    soil_dobson = make_soil(diel_model="dobson")
    soil_mironov = make_soil(diel_model="mironov")
    soil_wang = make_soil(diel_model="wang")
    print("\n7. Dielectric constant with different models:")
    print(f"Dobson model: {soil_dobson.dielectric_constant(sensor):.3f}")
    print(f"Mironov model: {soil_mironov.dielectric_constant(sensor):.3f}")
    print(f"Wang model: {soil_wang.dielectric_constant(sensor):.3f}")
    
    # Example 8: Create soil with bulk and specific density
    soil8 = make_soil(
        bulk_density=1.5,  # 1.5 g/cm³
        specific_density=2.65  # 2.65 g/cm³
    )
    print("\n8. Soil with density parameters:")
    print(soil8)

if __name__ == "__main__":
    main() 