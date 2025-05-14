"""
Layer module for CanORT (Canopy Optical Radiative Transfer) model.
This module defines the Layer class which represents a single layer in the canopy.
"""

import warnings
from typing import Optional
from .constants import *

class Layer:
    """A single layer in the vegetation canopy."""
    
    def __init__(self, 
                 thickness: float,
                 temperature: float,
                 leaf_thickness: float = DEFAULT_LEAF_THICKNESS,
                 water_volumetric_fraction: float = DEFAULT_WATER_VOLUMETRIC_FRACTION,
                 lai: float = DEFAULT_LAI,
                 dry_mass_density: Optional[float] = DEFAULT_DRY_MASS_DENSITY,
                 dielectric_constant: Optional[complex] = None):
        """
        Initialize a canopy layer.
        
        Args:
            thickness: Layer thickness (m)
            temperature: Layer temperature (K)
            leaf_thickness: Leaf thickness (mm)
            water_volumetric_fraction: Leaf Volumetric Moisture Content (m3/m3)
            lai: Leaf Area Index (m²/m²)
            dry_mass_density: Dry density of the solid material (g/cm³). Defaults to 0.3.
            dielectric_constant: Complex dielectric constant
        """
        # Validate input parameters
        if thickness < MIN_LAYER_THICKNESS or thickness > MAX_LAYER_THICKNESS:
            raise ValueError(f"Layer thickness must be between {MIN_LAYER_THICKNESS} and {MAX_LAYER_THICKNESS} meters")
        if lai < MIN_LAI or lai > MAX_LAI:
            raise ValueError(f"Leaf area index must be between {MIN_LAI} and {MAX_LAI}")
        if water_volumetric_fraction < ZERO or water_volumetric_fraction > ONE:
            raise ValueError(f"Water volumetric fraction must be between {ZERO} and {ONE}")
        
        self.thickness = thickness
        self.temperature = temperature
        self.leaf_thickness = leaf_thickness
        self.water_volumetric_fraction = water_volumetric_fraction
        self.lai = lai
        self.dry_mass_density = dry_mass_density
        self.dielectric_constant = dielectric_constant
    
    @property
    def layer_water_content(self) -> float:
        """Water content of the layer per unit area, in kg/m²"""
        #  Mw=Vw * rho_w * LAI * Ld 
        #  g/m2 = m3/m3 * kg/m3 * m2/m2 * mm * 1e-3 m/mm    
        return self.water_volumetric_fraction* WATER_DENSITY_KG_M3 * self.lai * self.leaf_thickness * MM_TO_M
    
    @property
    def lfmc(self) -> float:
        """Live fuel moisture content, in kg/kg"""
        # LFMC = Mw / Md 
        return self.layer_water_content / self.agb   
    
    @property
    def agb(self) -> float:
        """Above ground biomass, in kg/m²"""
        # Md=(1-Vw) * rho_d * LAI * Ld
        # kg/m2 = (1-m3/m3) * kg/m3 * m2/m2 * mm * 1e-3 m/mm    
        return (ONE - self.water_volumetric_fraction)*self.dry_mass_density * THOUSAND * self.lai * self.leaf_thickness * MM_TO_M
    
    def __str__(self):
        """String representation of the Layer object."""
        return (
            f"Layer(thickness={self.thickness:.2f}m, "
            f"LAI={self.lai:.2f}, leaf_thickness={self.leaf_thickness:.3f}mm, "
            f"temperature={self.temperature:.2f}K, water_volumetric_fraction={self.water_volumetric_fraction:.3f}, "
            f"dry_mass_density={self.dry_mass_density:.3f}g/cm³)"
        ) 