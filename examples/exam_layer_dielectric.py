"""
Example script demonstrating the comparison of different leaf dielectric models.

This script shows how to:
1. Create canopy layers with different dielectric models
2. Compare dielectric constants from different models
3. Visualize the results
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core.layer import Layer
from src.core.constants import *

def plot_dielectric_comparison(
    frequencies: np.ndarray,
    real_parts: dict,
    imag_parts: dict,
    title: str = "Leaf Dielectric Model Comparison"
):
    """Plot the real and imaginary parts of leaf dielectric constants for different models.
    
    Args:
        frequencies: Array of frequencies in GHz
        real_parts: Dictionary of real parts for different models
        imag_parts: Dictionary of imaginary parts for different models
        title: Plot title
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot real parts
    for model_name, values in real_parts.items():
        ax1.plot(frequencies, values, label=model_name)
    ax1.set_xlabel('Frequency (GHz)')
    ax1.set_ylabel('Real Part')
    ax1.set_title(f'{title} - Real Part')
    ax1.grid(True)
    ax1.legend()
    
    # Plot imaginary parts
    for model_name, values in imag_parts.items():
        ax2.plot(frequencies, values, label=model_name)
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('Imaginary Part')
    ax2.set_title(f'{title} - Imaginary Part')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(f"{title}.png")

def main():
    # Common layer properties
    common_params = {
        'thickness': 0.5,  # 0.5 meters
        'temperature': 293.15,  # 20°C
        'leaf_thickness': 0.17,  # 0.17 mm
        'water_volumetric_fraction': 0.6,  # 60% water by volume
        'lai': 2.0,  # Leaf Area Index of 2.0
        'dry_mass_density': 0.3,  # 0.3 g/cm³
        'effective_permittivity_model': 'maxwell_garnett'
    }
    
    # Create two layers with different dielectric models
    layer_ulaby = Layer(
        **common_params,
        diel_model='ulaby87'  # Ulaby & El Rayes model
    )
    
    layer_matzler = Layer(
        **common_params,
        diel_model='matzler94'  # Matzler model
    )
    
    # Print layer properties
    print("Layer Properties:")
    print("-" * 50)
    print(f"Thickness: {common_params['thickness']:.2f} m")
    print(f"Temperature: {common_params['temperature']-273.15:.1f}°C")
    print(f"Leaf thickness: {common_params['leaf_thickness']:.3f} mm")
    print(f"Water volumetric fraction: {common_params['water_volumetric_fraction']:.1%}")
    print(f"Leaf Area Index: {common_params['lai']:.2f}")
    print(f"Dry mass density: {common_params['dry_mass_density']:.2f} g/cm³")
    print()
    
    # Define frequency range
    frequencies = np.linspace(1, 37, 100)  # 1-37 GHz
    
    # Calculate dielectric constants
    real_parts = {}
    imag_parts = {}
    
    # Calculate for both models
    for layer, model_name in [(layer_ulaby, "Ulaby & El Rayes"), (layer_matzler, "Matzler")]:
        real_parts[model_name] = []
        imag_parts[model_name] = []
        
        for freq in frequencies:
            eps = layer.dielectric_constant(freq)
            real_parts[model_name].append(eps.real)
            imag_parts[model_name].append(eps.imag)
    
    # Convert lists to numpy arrays
    for model in real_parts:
        real_parts[model] = np.array(real_parts[model])
        imag_parts[model] = np.array(imag_parts[model])
    
    # Plot results
    plot_dielectric_comparison(
        frequencies,
        real_parts,
        imag_parts,
        f"Leaf Dielectric Model Comparison (VWC={common_params['water_volumetric_fraction']:.1%})"
    )
    
    # Print some specific values at 5 GHz
    print("\nDielectric constants at 5 GHz:")
    print("-" * 50)
    for model_name in real_parts:
        idx = np.abs(frequencies - 5).argmin()  # Find closest to 5 GHz
        print(f"{model_name}:")
        print(f"  Real part: {real_parts[model_name][idx]:.2f}")
        print(f"  Imaginary part: {imag_parts[model_name][idx]:.2f}")
        print(f"  Magnitude: {abs(complex(real_parts[model_name][idx], imag_parts[model_name][idx])):.2f}")
        print()

if __name__ == "__main__":
    main() 