"""
Example script for creating and testing soil types in CanORT.
This script demonstrates how to create different soil types and test their dielectric properties.

Example usage:
    python examples/example_make_soil.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.dielectrics.soil_dielectrics import SoilDiels

class SimpleSoil:
    """A simple implementation of the SoilLike protocol for testing."""
    def __init__(self, moisture, sand, clay, temperature, bulk_density, specific_density):
        self.moisture = moisture
        self.sand = sand
        self.clay = clay
        self.temperature = temperature
        self.bulk_density = bulk_density
        self.specific_density = specific_density

def create_soil_examples():
    """Create example soil types with different properties."""
    return {
        "Sandy Loam": SimpleSoil(
            moisture=0.25,      # 25% volumetric water content
            sand=0.5,          # 50% sand
            clay=0.2,          # 20% clay
            temperature=293.15, # 20°C
            bulk_density=1.3,   # g/cm³
            specific_density=2.65 # g/cm³
        ),
        "Clay Soil": SimpleSoil(
            moisture=0.35,      # 35% volumetric water content
            sand=0.2,          # 20% sand
            clay=0.6,          # 60% clay
            temperature=293.15, # 20°C
            bulk_density=1.4,   # g/cm³
            specific_density=2.65 # g/cm³
        ),
        "Sandy Soil": SimpleSoil(
            moisture=0.15,      # 15% volumetric water content
            sand=0.8,          # 80% sand
            clay=0.1,          # 10% clay
            temperature=293.15, # 20°C
            bulk_density=1.2,   # g/cm³
            specific_density=2.65 # g/cm³
        )
    }

def print_soil_properties(soil, name):
    """Print soil properties in a formatted way."""
    print(f"\n{name} Properties:")
    print("-" * 40)
    print(f"Moisture:     {soil.moisture:.2f} m³/m³")
    print(f"Sand:         {soil.sand:.2f}")
    print(f"Clay:         {soil.clay:.2f}")
    print(f"Temperature:  {soil.temperature-273.15:.1f}°C")
    print(f"Bulk density: {soil.bulk_density:.2f} g/cm³")

def test_dielectric_models(soil, frequencies):
    """Test different dielectric models for given soil and frequencies."""
    print("\nDielectric Constants:")
    print("=" * 60)
    
    for freq in frequencies:
        print(f"\nFrequency: {freq:.1f} GHz")
        print("-" * 40)
        
        # Test each model
        for model_name in ["dobson85", "mironov04", "wang80"]:
            model = SoilDiels.get_model(model_name)
            eps = model(soil, freq)
            print(f"{model_name:10s}: {eps.real:6.2f} + {eps.imag:6.2f}j")

def main():
    """Main function to run the soil creation and dielectric testing."""
    print("Soil Creation and Dielectric Testing")
    print("===================================")
    
    # Create example soils
    soils = create_soil_examples()
    
    # Test frequencies (GHz)
    frequencies = [1.4, 5.0, 10.0]
    
    # Test each soil type
    for soil_name, soil in soils.items():
        print(f"\n{soil_name}")
        print("=" * 40)
        print_soil_properties(soil, soil_name)
        test_dielectric_models(soil, frequencies)

if __name__ == "__main__":
    main() 