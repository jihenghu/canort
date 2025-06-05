"""
Example script demonstrating the calculation of effective permittivity for different canopy layers.
This example shows how to create Layer objects with different configurations and calculate their
effective permittivity at various frequencies.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.core.layer import Layer

def plot_effective_permittivity(frequencies, real_parts, imag_parts, labels, title):
    """Helper function to plot effective permittivity results."""
    plt.figure(figsize=(12, 5))
    
    # Plot real part
    plt.subplot(1, 2, 1)
    for real, label in zip(real_parts, labels):
        plt.plot(frequencies, real, label=label)
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Real Part')
    plt.title(f'{title} - Real Part')
    plt.legend()
    plt.grid(True)
    
    # Plot imaginary part
    plt.subplot(1, 2, 2)
    for imag, label in zip(imag_parts, labels):
        plt.plot(frequencies, imag, label=label)
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Imaginary Part')
    plt.title(f'{title} - Imaginary Part')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'{title}.png')

def main():
    # Define frequency range
    frequencies = np.linspace(1, 10, 100)  # 1-10 GHz
    
    # Example 1: Compare different leaf types
    print("\nExample 1: Comparing different leaf types")
    layers = [
        Layer(thickness=1.0, temperature=293.15, leaf_type='disk', 
              water_volumetric_fraction=0.5, lai=2.0, effective_permittivity_model='power_law'),
              
        Layer(thickness=1.0, temperature=293.15, leaf_type='sphere',
              water_volumetric_fraction=0.5, lai=2.0, effective_permittivity_model='typemodel'),
        Layer(thickness=1.0, temperature=293.15, leaf_type='needle',
              water_volumetric_fraction=0.5, lai=2.0, effective_permittivity_model='typemodel'),
        Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
              water_volumetric_fraction=0.5, lai=2.0, effective_permittivity_model='typemodel')
    ]
    
    real_parts = []
    imag_parts = []
    labels = []
    
    for layer in layers:
        permittivities = [layer.effective_permittivity(f) for f in frequencies]
        real_parts.append([p.real for p in permittivities])
        imag_parts.append([p.imag for p in permittivities])
        labels.append(f"{layer.leaf_type} (model={layer.effective_permittivity_model})")
    
    plot_effective_permittivity(frequencies, real_parts, imag_parts, labels,
                              "Effective Permittivity vs Leaf Type")
    
    # Example 2: Compare different moisture contents
    print("\nExample 2: Comparing different moisture contents")
    layers = [
        Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
              water_volumetric_fraction=0.3, lai=2.0),
        Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
              water_volumetric_fraction=0.5, lai=2.0),
        Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
              water_volumetric_fraction=0.7, lai=2.0)
    ]
    
    real_parts = []
    imag_parts = []
    labels = []
    
    for layer in layers:
        permittivities = [layer.effective_permittivity(f) for f in frequencies]
        real_parts.append([p.real for p in permittivities])
        imag_parts.append([p.imag for p in permittivities])
        labels.append(f"VWC={layer.water_volumetric_fraction}")
    
    plot_effective_permittivity(frequencies, real_parts, imag_parts, labels,
                              "Effective Permittivity vs Moisture Content")
    
    # # Example 3: Compare different dielectric models
    # print("\nExample 3: Comparing different dielectric models")
    # layers = [
    #     Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
    #           water_volumetric_fraction=0.5, lai=2.0, diel_model='matzler94'),
    #     Layer(thickness=1.0, temperature=293.15, leaf_type='disk',
    #           water_volumetric_fraction=0.5, lai=2.0, diel_model='ulaby87')
    # ]
    
    # real_parts = []
    # imag_parts = []
    # labels = []
    
    # for layer in layers:
    #     permittivities = [layer.effective_permittivity(f) for f in frequencies]
    #     real_parts.append([p.real for p in permittivities])
    #     imag_parts.append([p.imag for p in permittivities])
    #     labels.append(f"{layer.diel_model} model")
    
    # plot_effective_permittivity(frequencies, real_parts, imag_parts, labels,
    #                           "Effective Permittivity vs Dielectric Model")

if __name__ == "__main__":
    main() 