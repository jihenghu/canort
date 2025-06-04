"""
Effective dielectric models module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides dielectric constant calculations for vegetation using different mixing models.
"""

from typing import Callable, Dict, Literal, Protocol, runtime_checkable
import numpy as np
from .water_dielectrics import WaterDiels
from ..core.constants import *

@runtime_checkable
class LeafLike(Protocol):
    """Protocol defining the interface for leaf-like objects."""
    water_volumetric_fraction: float
    temperature: float
    dry_mass_density: float

class EffectivePermittivityModels:
    """A class containing different leaf dielectric models."""
    
    @staticmethod
    def linear_mixing(
        leaf: LeafLike,
        frequency: float
    ) -> complex:
        """Simple linear mixing model for leaf dielectric constant.
        
        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(leaf.temperature, frequency)
        
        # Calculate leaf dielectric constant using linear mixing
        leaf_diel = (1 - leaf.water_volumetric_fraction) * AIR_DIELECTRIC + \
                   leaf.water_volumetric_fraction * water_diel
        
        return leaf_diel
    
    @staticmethod
    def maxwell_garnett(
        leaf: LeafLike,
        frequency: float
    ) -> complex:
        """Maxwell-Garnett mixing model for leaf dielectric constant.
        
        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(leaf.temperature, frequency)
        
        # Calculate leaf dielectric constant using Maxwell-Garnett mixing
        f = leaf.water_volumetric_fraction
        leaf_diel = AIR_DIELECTRIC * (1 + 2 * f * (water_diel - AIR_DIELECTRIC) / 
                                    (water_diel + 2 * AIR_DIELECTRIC - 
                                     f * (water_diel - AIR_DIELECTRIC)))
        
        return leaf_diel
    
    @staticmethod
    def bruggeman(
        leaf: LeafLike,
        frequency: float
    ) -> complex:
        """Bruggeman mixing model for leaf dielectric constant.
        
        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(leaf.temperature, frequency)
        
        # Calculate leaf dielectric constant using Bruggeman mixing
        f = leaf.water_volumetric_fraction
        leaf_diel = 0.25 * (water_diel * (2 * f - 1) + AIR_DIELECTRIC * (1 - 2 * f) +
                           np.sqrt((water_diel * (2 * f - 1) + AIR_DIELECTRIC * (1 - 2 * f))**2 +
                                  8 * water_diel * AIR_DIELECTRIC))
        
        return leaf_diel
    
    @classmethod
    def get_model(cls, model_name: Literal["linear", "maxwell_garnett", "bruggeman"]) -> Callable:
        """Get the specified dielectric model function.
        
        Args:
            model_name: Name of the dielectric model to use
            
        Returns:
            Callable: The requested dielectric model function
            
        Raises:
            ValueError: If the model name is not recognized
        """
        models: Dict[str, Callable] = {
            "linear": cls.linear_mixing,
            "maxwell_garnett": cls.maxwell_garnett,
            "bruggeman": cls.bruggeman
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown dielectric model: {model_name}")
            
        return models[model_name] 