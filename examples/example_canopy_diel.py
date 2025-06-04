"""
Example script demonstrating the usage of canopy creation and dielectric calculations in CanORT.
This script shows how to create different types of canopy layers and calculate their dielectric properties.
"""

import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.io.make_medium import make_layer, make_canopy, create_uniform_canopy
from src.io.sensor_list import smap

def main():
    # Example 1: Create a single layer with default parameters
    layer1 = make_layer(
        thickness=1.0,  # 1 meter
        temperature=293.15  # 20°C
    )
    print("\n1. Single layer with default parameters:")
    print(layer1)
    
    # Example 2: Create a layer with custom parameters
    layer2 = make_layer(
        thickness=0.5,  # 0.5 meters
        temperature=298.15,  # 25°C
        leaf_thickness=0.2,  # 0.2 mm
        water_volumetric_fraction=0.7,  # 70% water content
        lai=2.0,  # LAI of 2
        dry_mass_density=0.3,  # 0.3 g/cm³
        diel_model="maxwell_garnett"
    )
    print("\n2. Layer with custom parameters:")
    print(layer2)
    
    # Example 3: Create a canopy with multiple layers
    canopy1 = make_canopy(
        thicknesses=[0.5, 1.0, 0.5],  # Three layers: 0.5m, 1.0m, 0.5m
        temperatures=[293.15, 295.15, 297.15],  # Increasing temperature with height
        leaf_thicknesses=[0.15, 0.2, 0.15],  # Thicker leaves in middle layer
        water_volumetric_fractions=[0.6, 0.7, 0.6],  # More water in middle layer
        lais=[1.5, 2.0, 1.5],  # Higher LAI in middle layer
        dry_mass_densities=[0.3, 0.3, 0.3],  # Same dry mass density
        diel_models=["linear", "maxwell_garnett", "bruggeman"]  # Different models
    )
    print("\n3. Canopy with three layers:")
    print(canopy1)
    
    # Example 4: Create a uniform canopy
    canopy2 = create_uniform_canopy(
        n_layers=5,  # 5 layers
        total_thickness=2.0,  # 2 meters total
        temperature=293.15,  # 20°C
        leaf_thickness=0.2,  # 0.2 mm
        water_volumetric_fraction=0.6,  # 60% water content
        total_lai=3.0,  # Total LAI of 3
        dry_mass_density=0.3  # 0.3 g/cm³
    )
    print("\n4. Uniform canopy with 5 layers:")
    print(canopy2)
    
    # Example 5: Calculate dielectric properties
    sensor = smap()  # Use SMAP sensor configuration
    print("\n5. Dielectric properties at SMAP frequency:")
    
    # Calculate for each layer in canopy1
    print("\nLayer dielectric constants:")
    for i, layer in enumerate(canopy1.layers):
        diel = layer.dielectric_constant(sensor.frequency)
        eff_diel = layer.effective_permittivity(sensor.frequency)
        print(f"Layer {i+1}:")
        print(f"  Dielectric constant: {diel:.3f}")
        print(f"  Effective permittivity: {eff_diel:.3f}")
    
    # Example 6: Compare different dielectric models
    print("\n6. Comparison of dielectric models:")
    models = ["linear", "maxwell_garnett", "bruggeman"]
    for model in models:
        layer = make_layer(
            thickness=1.0,
            temperature=293.15,
            water_volumetric_fraction=0.7,
            lai=2.0,
            diel_model=model
        )
        diel = layer.dielectric_constant(sensor.frequency)
        eff_diel = layer.effective_permittivity(sensor.frequency)
        print(f"\n{model.capitalize()} model:")
        print(f"  Dielectric constant: {diel:.3f}")
        print(f"  Effective permittivity: {eff_diel:.3f}")
    
    # Example 7: Effect of water content
    print("\n7. Effect of water content on dielectric properties:")
    water_contents = [0.3, 0.5, 0.7, 0.9]
    for wc in water_contents:
        layer = make_layer(
            thickness=1.0,
            temperature=293.15,
            water_volumetric_fraction=wc,
            lai=2.0,
            diel_model="maxwell_garnett"
        )
        diel = layer.dielectric_constant(sensor.frequency)
        eff_diel = layer.effective_permittivity(sensor.frequency)
        print(f"\nWater content {wc*100}%:")
        print(f"  Dielectric constant: {diel:.3f}")
        print(f"  Effective permittivity: {eff_diel:.3f}")

if __name__ == "__main__":
    main() 