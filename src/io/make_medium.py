"""
Functions for creating canopy layers and structures.
"""

from typing import List, Optional, Dict, Any
import numpy as np

from ..core.layer import Layer
from ..core.canopy import Canopy
from ..core.constants import *

def make_layer(
    thickness: float,
    temperature: float,
    leaf_thickness: float = DEFAULT_LEAF_THICKNESS,
    water_volumetric_fraction: float = DEFAULT_WATER_VOLUMETRIC_FRACTION,
    lai: float = DEFAULT_LAI,
    dry_mass_density: Optional[float] = DEFAULT_DRY_MASS_DENSITY,
    dielectric_constant: Optional[complex] = None,
    properties: Optional[Dict[str, Any]] = None
) -> Layer:
    """
    Create a single canopy layer.
    
    Args:
        thickness: Layer thickness (m)
        temperature: Layer temperature (K)
        leaf_thickness: Leaf thickness (mm)
        water_volumetric_fraction: Water volumetric fraction (m3/m3)
        lai: Leaf Area Index (m²/m²)
        dry_mass_density: Dry density of the solid material (g/cm³)
        dielectric_constant: Complex dielectric constant
        properties: Additional layer properties
    
    Returns:
        Layer: A canopy layer object
    """
    layer = Layer(
        thickness=thickness,
        temperature=temperature,
        leaf_thickness=leaf_thickness,
        water_volumetric_fraction=water_volumetric_fraction,
        lai=lai,
        dry_mass_density=dry_mass_density,
        dielectric_constant=dielectric_constant
    )
    
    if properties:
        for key, value in properties.items():
            setattr(layer, key, value)
    
    return layer

def make_canopy(
    thicknesses: List[float],
    temperatures: List[float],
    leaf_thicknesses: Optional[List[float]] = None,
    water_volumetric_fractions: Optional[List[float]] = None,
    lais: Optional[List[float]] = None,
    dry_mass_densities: Optional[List[float]] = None,
    dielectric_constants: Optional[List[complex]] = None
) -> Canopy:
    """
    Create a canopy with multiple layers.
    
    Args:
        thicknesses: List of layer thicknesses (m)
        temperatures: List of layer temperatures (K)
        leaf_thicknesses: List of leaf thicknesses (mm)
        water_volumetric_fractions: List of water volumetric fractions (m3/m3)
        lais: List of leaf area indices (m²/m²)
        dry_mass_densities: List of dry mass densities (g/cm³)
        dielectric_constants: List of complex dielectric constants
    
    Returns:
        Canopy: A canopy object with the specified layers
    """
    n_layers = len(thicknesses)
    
    # Validate input arrays have the same length
    if len(temperatures) != n_layers:
        raise ValueError("temperatures must have the same length as thicknesses")
    if leaf_thicknesses is not None and len(leaf_thicknesses) != n_layers:
        raise ValueError("leaf_thicknesses must have the same length as thicknesses")
    if water_volumetric_fractions is not None and len(water_volumetric_fractions) != n_layers:
        raise ValueError("water_volumetric_fractions must have the same length as thicknesses")
    if lais is not None and len(lais) != n_layers:
        raise ValueError("lais must have the same length as thicknesses")
    if dry_mass_densities is not None and len(dry_mass_densities) != n_layers:
        raise ValueError("dry_mass_densities must have the same length as thicknesses")
    if dielectric_constants is not None and len(dielectric_constants) != n_layers:
        raise ValueError("dielectric_constants must have the same length as thicknesses")
    
    # Create layers
    layers = []
    for i in range(n_layers):
        layer = make_layer(
            thickness=thicknesses[i],
            temperature=temperatures[i],
            leaf_thickness=leaf_thicknesses[i] if leaf_thicknesses is not None else 0.2,
            water_volumetric_fraction=water_volumetric_fractions[i] if water_volumetric_fractions is not None else 0.5,
            lai=lais[i] if lais is not None else 1.0,
            dry_mass_density=dry_mass_densities[i] if dry_mass_densities is not None else 0.3,
            dielectric_constant=dielectric_constants[i] if dielectric_constants is not None else None
        )
        layers.append(layer)
    
    return Canopy(layers=layers)

def create_uniform_canopy(
    n_layers: int,
    total_thickness: float,
    temperature: float = DEFAULT_TEMPERATURE,
    leaf_thickness: float = DEFAULT_LEAF_THICKNESS,
    water_volumetric_fraction: float = DEFAULT_WATER_VOLUMETRIC_FRACTION,
    total_lai: float = DEFAULT_LAI,
    dry_mass_density: float = DEFAULT_DRY_MASS_DENSITY
) -> Canopy:
    """
    Create a canopy with uniform layer properties.
    
    Args:
        n_layers: Number of layers
        total_thickness: Total canopy thickness (m)
        temperature: Layer temperature (K)
        leaf_thickness: Leaf thickness (mm)
        water_volumetric_fraction: Water volumetric fraction (m3/m3)
        total_lai: Total leaf area index (m²/m²)
        dry_mass_density: Dry mass density (g/cm³)
    
    Returns:
        Canopy: A canopy with uniform layer properties
    """
    # Create uniform arrays
    thicknesses = [total_thickness / n_layers] * n_layers
    temperatures = [temperature] * n_layers
    leaf_thicknesses = [leaf_thickness] * n_layers
    water_volumetric_fractions = [water_volumetric_fraction] * n_layers
    lais = [total_lai / n_layers] * n_layers
    dry_mass_densities = [dry_mass_density] * n_layers
    
    return make_canopy(
        thicknesses=thicknesses,
        temperatures=temperatures,
        leaf_thicknesses=leaf_thicknesses,
        water_volumetric_fractions=water_volumetric_fractions,
        lais=lais,
        dry_mass_densities=dry_mass_densities
    ) 