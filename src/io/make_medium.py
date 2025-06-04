"""
Functions for creating canopy layers and structures.
"""

from typing import List, Optional, Dict, Any, Literal
import numpy as np

from ..core.layer import Layer
from ..core.canopy import Canopy
from ..core.constants import *
from ..core.soil import Soil

def make_layer(
    thickness: float,
    temperature: float,
    leaf_thickness: float = 0.2,
    water_volumetric_fraction: float = 0.6,
    lai: float = 1.0,
    dry_mass_density: Optional[float] = 0.3,
    diel_model: Literal['linear', 'maxwell_garnett', 'bruggeman'] = 'linear'
) -> Layer:
    """
    Create a single layer with specified parameters.
    
    Args:
        thickness: Layer thickness in meters
        temperature: Layer temperature in Kelvin
        leaf_thickness: Leaf thickness in mm
        water_volumetric_fraction: Leaf volumetric moisture content (m³/m³)
        lai: Leaf area index (m²/m²)
        dry_mass_density: Dry mass density in g/cm³
        diel_model: Dielectric mixing model to use
        
    Returns:
        Layer: A new Layer instance
    """
    layer = Layer(
        thickness=thickness,
        temperature=temperature,
        leaf_thickness=leaf_thickness,
        water_volumetric_fraction=water_volumetric_fraction,
        lai=lai,
        dry_mass_density=dry_mass_density,
        diel_model=diel_model
    )
    return layer

def make_canopy(
    thicknesses: List[float],
    temperatures: List[float],
    leaf_thicknesses: Optional[List[float]] = None,
    water_volumetric_fractions: Optional[List[float]] = None,
    lais: Optional[List[float]] = None,
    dry_mass_densities: Optional[List[float]] = None,
    diel_models: Optional[List[Literal['linear', 'maxwell_garnett', 'bruggeman']]] = None
) -> Canopy:
    """
    Create a canopy with multiple layers.
    
    Args:
        thicknesses: List of layer thicknesses in meters
        temperatures: List of layer temperatures in Kelvin
        leaf_thicknesses: List of leaf thicknesses in mm
        water_volumetric_fractions: List of leaf volumetric moisture contents (m³/m³)
        lais: List of leaf area indices (m²/m²)
        dry_mass_densities: List of dry mass densities in g/cm³
        diel_models: List of dielectric mixing models to use
        
    Returns:
        Canopy: A new Canopy instance
    """
    n_layers = len(thicknesses)
    
    # Set default values if not provided
    if leaf_thicknesses is None:
        leaf_thicknesses = [0.2] * n_layers
    if water_volumetric_fractions is None:
        water_volumetric_fractions = [0.6] * n_layers
    if lais is None:
        lais = [1.0] * n_layers
    if dry_mass_densities is None:
        dry_mass_densities = [0.3] * n_layers
    if diel_models is None:
        diel_models = ['linear'] * n_layers
    
    # Create layers
    layers = []
    for i in range(n_layers):
        layer = make_layer(
            thickness=thicknesses[i],
            temperature=temperatures[i],
            leaf_thickness=leaf_thicknesses[i],
            water_volumetric_fraction=water_volumetric_fractions[i],
            lai=lais[i],
            dry_mass_density=dry_mass_densities[i],
            diel_model=diel_models[i]
        )
        layers.append(layer)
    
    return Canopy(layers=layers)

def create_uniform_canopy(
    n_layers: int,
    total_thickness: float,
    temperature: float,
    leaf_thickness: float = 0.2,
    water_volumetric_fraction: float = 0.6,
    total_lai: float = 3.0,
    dry_mass_density: float = 0.3,
    diel_model: Literal['linear', 'maxwell_garnett', 'bruggeman'] = 'linear'
) -> Canopy:
    """
    Create a uniform canopy with evenly distributed properties.
    
    Args:
        n_layers: Number of layers
        total_thickness: Total canopy thickness in meters
        temperature: Layer temperature in Kelvin
        leaf_thickness: Leaf thickness in mm
        water_volumetric_fraction: Leaf volumetric moisture content (m³/m³)
        total_lai: Total leaf area index (m²/m²)
        dry_mass_density: Dry mass density in g/cm³
        diel_model: Dielectric mixing model to use
        
    Returns:
        Canopy: A new Canopy instance with uniform properties
    """
    layer_thickness = total_thickness / n_layers
    layer_lai = total_lai / n_layers
    
    thicknesses = [layer_thickness] * n_layers
    temperatures = [temperature] * n_layers
    leaf_thicknesses = [leaf_thickness] * n_layers
    water_volumetric_fractions = [water_volumetric_fraction] * n_layers
    lais = [layer_lai] * n_layers
    dry_mass_densities = [dry_mass_density] * n_layers
    diel_models = [diel_model] * n_layers
    
    return make_canopy(
        thicknesses=thicknesses,
        temperatures=temperatures,
        leaf_thicknesses=leaf_thicknesses,
        water_volumetric_fractions=water_volumetric_fractions,
        lais=lais,
        dry_mass_densities=dry_mass_densities,
        diel_models=diel_models
    ) 