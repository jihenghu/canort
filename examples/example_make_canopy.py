"""
Example script demonstrating how to create and manipulate canopy layers.
"""

import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.io.make_medium import make_layer, make_canopy, create_uniform_canopy

# Create a sample canopy with multiple layers
thicknesses = [0.5, 1.0, 0.5]  # meters
temperatures = [290.0, 295.0, 300.0]  # Kelvin
leaf_thicknesses = [0.1, 0.2, 0.1]  # mm
water_volumetric_fractions = [0.2, 0.3, 0.2]  # m3/m3
lais = [0.8, 1.2, 0.8]  # m2/m2
dry_mass_densities = [0.25, 0.3, 0.25]  # g/cm3

# Create the canopy
canopy = make_canopy(
    thicknesses=thicknesses,
    temperatures=temperatures,
    leaf_thicknesses=leaf_thicknesses,
    water_volumetric_fractions=water_volumetric_fractions,
    lais=lais,
    dry_mass_densities=dry_mass_densities
)

# Print canopy information
print("\nSample Canopy:")
print(canopy)

# Create a uniform canopy
uniform_canopy = create_uniform_canopy(
    n_layers=3,
    total_thickness=2.0,
    temperature=295.0,
    leaf_thickness=0.2,
    water_volumetric_fraction=0.5,
    total_lai=4.2,
    dry_mass_density=0.3
)

# Print uniform canopy information
print("\nUniform Canopy:")
print(uniform_canopy)
