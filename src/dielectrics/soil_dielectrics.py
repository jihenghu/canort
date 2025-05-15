"""
Soil dielectric models module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides dielectric constant calculations for soil using different models.
"""

from typing import Callable, Dict, Literal, Protocol, runtime_checkable
import numpy as np
from .water_dielectrics import WaterDiels

@runtime_checkable
class SoilLike(Protocol):
    """Protocol defining the interface for soil-like objects."""
    moisture: float
    sand: float
    clay: float
    temperature: float
    bulk_density: float
    specific_density: float

class SoilDiels:
    """A class containing different soil dielectric models."""
    
    @staticmethod
    def dobson_model(
        soil: SoilLike,
        frequency: float
    ) -> complex:
        """Dobson et al. (1985) dielectric model for soil.
        
        Args:
            soil: Soil-like object containing moisture, sand, clay, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate porosity
        porosity = 1 - soil.bulk_density / soil.specific_density
        
        # Calculate bound water fraction
        bound_water = 0.06774 - 0.06473 * soil.sand + 0.478 * soil.clay
        
        # Calculate free water fraction
        free_water = soil.moisture - bound_water
        if free_water < 0:
            free_water = 0
        
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(soil.temperature, frequency)
        
        # Calculate soil dielectric constant
        soil_diel = (1 + 0.65 * soil.bulk_density + soil.moisture**0.65 * water_diel - soil.moisture)**2
        soil_diel = np.sqrt(soil_diel)
        
        return soil_diel
    
    @staticmethod
    def mironov_model(
        soil: SoilLike,
        frequency: float
    ) -> complex:
        """Mironov et al. (2009) dielectric model for soil.
        
        Args:
            soil: Soil-like object containing moisture, sand, clay, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(soil.temperature, frequency)
        
        # Calculate soil dielectric constant
        soil_diel = 1 + (water_diel - 1) * soil.moisture
        
        return soil_diel
    
    @staticmethod
    def wang_model(
        soil: SoilLike,
        frequency: float
    ) -> complex:
        """Wang and Schmugge (1980) dielectric model for soil.
        
        Args:
            soil: Soil-like object containing moisture, sand, clay, temperature, and density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        water_diel = WaterDiels.debye(soil.temperature, frequency)
        
        # Calculate soil dielectric constant
        soil_diel = 1 + (water_diel - 1) * soil.moisture
        
        return soil_diel
    
    @classmethod
    def get_model(cls, model_name: Literal["dobson", "mironov", "wang"]) -> Callable:
        """Get the specified dielectric model function.
        
        Args:
            model_name: Name of the dielectric model to use
            
        Returns:
            Callable: The requested dielectric model function
            
        Raises:
            ValueError: If the model name is not recognized
        """
        models: Dict[str, Callable] = {
            "dobson": cls.dobson_model,
            "mironov": cls.mironov_model,
            "wang": cls.wang_model
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown dielectric model: {model_name}")
            
        return models[model_name] 