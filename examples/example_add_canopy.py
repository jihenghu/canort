"""
Example script demonstrating how to combine canopies using the addition operator.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.io.make_medium import make_canopy, create_uniform_canopy

# Create two different canopies
# First canopy: 2 layers with varying properties
canopy1 = make_canopy(
    thicknesses=[0.5, 0.5],  # meters
    temperatures=[290.0, 295.0],  # Kelvin
    leaf_thicknesses=[0.1, 0.2],  # mm
    water_volumetric_fractions=[0.4, 0.5],  # m3/m3
    lais=[0.8, 1.2],  # m2/m2
    dry_mass_densities=[0.25, 0.3]  # g/cm3
)

# Second canopy: uniform canopy with 3 layers
canopy2 = create_uniform_canopy(
    n_layers=3,
    total_thickness=1.5,
    temperature=300.0,
    leaf_thickness=0.15,
    water_volumetric_fraction=0.6,
    total_lai=4.2,
    dry_mass_density=0.35
)

# Print original canopies
print("\nFirst Canopy:")
print(canopy1)
print("\nSecond Canopy:")
print(canopy2)

# Combine canopies using the addition operator
combined_canopy = canopy1 + canopy2

# Print the combined canopy
print("\nCombined Canopy (First + Second):")
print(combined_canopy)

# Verify the properties of the combined canopy
print("\nVerification:")
print(f"Total number of layers: {combined_canopy.nlayers} (Expected: {canopy1.nlayers + canopy2.nlayers})")
print(f"Total thickness: {combined_canopy.thickness:.2f}m (Expected: {canopy1.thickness + canopy2.thickness:.2f}m)")
print(f"Total LAI: {combined_canopy.LAI:.2f} (Expected: {canopy1.LAI + canopy2.LAI:.2f})")
print(f"Total AGB: {combined_canopy.total_agb:.2f}kg/m² (Expected: {canopy1.total_agb + canopy2.total_agb:.2f}kg/m²)")
print(f"Total VWC: {combined_canopy.total_vwc:.2f}kg/m² (Expected: {canopy1.total_vwc + canopy2.total_vwc:.2f}kg/m²)") 