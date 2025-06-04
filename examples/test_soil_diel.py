"""
Example script demonstrating the comparison of different soil dielectric models.

This script shows how to:
1. Create soil layers with different dielectric models
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

from src.core.soil import Soil
from src.core.constants import *

def plot_soil_dielectric_comparison(
    frequencies: np.ndarray,
    real_parts: dict,
    imag_parts: dict,
    title: str = "Soil Dielectric Model Comparison"
):
    """Plot the real and imaginary parts of soil dielectric constants for different models.
    
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
    # Common soil properties
    common_params = {
        'temperature': 293.15,  # 20°C
        'moisture': 0.25,  # 25% volumetric water content
        'sand': 0.5,  # 50% sand
        'clay': 0.3,  # 30% clay
        
    }
    
    # Create soil layers with different dielectric models
    layer_dobson = Soil(
        **common_params,
        diel_model='dobson85'  # Dobson model
    )
    
    layer_mironov = Soil(
        **common_params,
        diel_model='mironov04'  # Mironov model
    )

    layer_wang = Soil(
        **common_params,
        diel_model='wang80'  # Wang model
    )
    
    # Print soil properties
    print("Soil Properties:")
    print("-" * 50)
    print(f"Temperature: {common_params['temperature']-273.15:.1f}°C")
    print(f"Soil water content: {common_params['moisture']:.1%}")
    print(f"Sand fraction: {common_params['sand']:.1%}")
    print(f"Clay fraction: {common_params['clay']:.1%}")
    print()
    
    # Define frequency range
    frequencies = np.linspace(1, 20, 100)  # 1-20 GHz
    
    # Calculate dielectric constants
    real_parts = {}
    imag_parts = {}
    
    # Calculate for both models 'dobson85', 'mironov04', 'wang80
    for layer, model_name in [(layer_dobson, "dobson85"), (layer_mironov, "mironov04"), (layer_wang, "wang80")  ]:
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
    plot_soil_dielectric_comparison(
        frequencies,
        real_parts,
        imag_parts,
        f"Soil Dielectric Model Comparison (VWC={common_params['moisture']:.1%})"
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