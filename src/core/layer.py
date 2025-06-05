"""
Layer module for CanORT (Canopy Optical Radiative Transfer) model.
This module defines the Layer class which represents a single layer in the canopy.
"""

import warnings
from typing import Optional, Literal
from .constants import *
from ..dielectrics.leaf_dielectrics import LeafDiels
from ..dielectrics.effective_dielectrics import EffectivePermittivityModels

class Layer:
    """A single layer in the vegetation canopy."""
    
    def __init__(self, 
                 thickness: float,
                 temperature: float,
                 leaf_type: Literal['needle', 'sphere', 'disk'] = 'disk',
                 leaf_thickness: float = DEFAULT_LEAF_THICKNESS,
                 water_volumetric_fraction: float = DEFAULT_WATER_VOLUMETRIC_FRACTION,
                 lai: float = DEFAULT_LAI,
                 dry_mass_density: Optional[float] = DEFAULT_DRY_MASS_DENSITY,
                 diel_model: Literal['ulaby87', 'matzler94'] = 'matzler94',
                 effective_permittivity_model: Literal['power_law', 'typemodel'] = 'power_law'):
        """
        Initialize a canopy layer.
        
        Args:
            thickness: Layer thickness (m)
            temperature: Layer temperature (K)
            leaf_type: Type of leaf shape ('needle', 'sphere', or 'disk'), defaults to 'disk'
            leaf_thickness: Leaf thickness (mm)
            water_volumetric_fraction: Leaf Volumetric Moisture Content (m3/m3)
            lai: Leaf Area Index (m²/m²)
            dry_mass_density: Dry density of the solid material (g/cm³). Defaults to 0.3.
            diel_model: Dielectric mixing model to use ('ulaby87' or 'matzler94')
            effective_permittivity_model: Effective permittivity model to use ('power_law', 'typemodel')
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
        self.leaf_type = leaf_type  ## TODO: Mixed phases of leaves
        # self.dewc=dewc  # TODO: dew and snow gannuals intercepted by the leaves
        self.leaf_thickness = leaf_thickness
        self.water_volumetric_fraction = water_volumetric_fraction
        self.lai = lai
        self.dry_mass_density = dry_mass_density
        self.diel_model = diel_model
        self.effective_permittivity_model = effective_permittivity_model
    

    def dielectric_constant(self, frequency: float) -> complex:
        """
        Calculate the complex dielectric constant of the layer.
        
        Args:
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        diel_const_func = LeafDiels.get_model(self.diel_model)
        if diel_const_func is None:
            raise ValueError(f"Unknown dielectric model: {self.diel_model}")
        return diel_const_func(self, frequency)
    

    def effective_permittivity(self, frequency: float) -> complex:
        """
        Calculate the effective permittivity of the layer considering leaf volume density.
        
        The effective permittivity is calculated using a mixing model that accounts for:
        1. The dielectric constant of the leaf material
        2. The volume fraction of leaves in the layer
        3. The air gaps between leaves
        
        Args:
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Effective permittivity of the layer
        """
        if self.effective_permittivity_model == 'power_law':
            eff_diel_func = EffectivePermittivityModels.get_model('power_law')
        elif self.effective_permittivity_model == 'typemodel':
            if self.leaf_type == 'sphere':
                eff_diel_func = EffectivePermittivityModels.get_model('spheric')
            elif self.leaf_type in ['needle', 'disk']:
                eff_diel_func = EffectivePermittivityModels.get_model('nonspheric')
        else:
            raise ValueError(f"Unknown effective permittivity model: {self.effective_permittivity_model}")
        
        if eff_diel_func is None:
            raise ValueError(f"Unknown effective permittivity model: {self.effective_permittivity_model}")
        
        return eff_diel_func(self, frequency)

    @property
    def leaf_volumetric_fraction(self) -> float:
        """Leaf volumetric fraction occupies in the layer"""
        return self.lai * self.leaf_thickness * MM_TO_M / self.thickness
    
    @property
    def water_gravimetric_fraction(self) -> float:
        """moisture content on a gravimetric wet-weight basis (mg), in g/g
        (4.71a) of Ulaby and Long (2014)
        """
        mv=self.water_volumetric_fraction  # cm3/cm3
        rhob=self.dry_mass_density # g/cm3
        mg=mv/(mv+(1-mv)*rhob)  # g/g
        return mg

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