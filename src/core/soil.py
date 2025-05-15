"""
Soil module for CanORT (Canopy Optical Radiative Transfer) model.
This module defines the Soil class which represents the soil surface properties.
"""

from typing import Literal, Optional
from .constants import *
from ..dielectrics.soil_dielectrics import SoilDiels
from .sensor import Sensor

class Soil:
    """A class representing soil surface properties."""
    
    def __init__(self,
                 temperature: float,
                 moisture: float = DEFAULT_SOIL_MOISTURE,
                 sand: float = DEFAULT_SAND_FRACTION,
                 clay: float = DEFAULT_CLAY_FRACTION,
                 diel_model: Literal['dobson', 'mironov', 'wang'] = 'dobson',
                 rms_hgt: Optional[float] = DEFAULT_RMS_HGT,
                 corr_length: Optional[float] = DEFAULT_CORR_LENGTH,
                 bulk_density: Optional[float] = DEFAULT_SOIL_BULK_DENSITY,
                 specific_density: Optional[float] = DEFAULT_SOIL_SPECIFIC_DENSITY):
        """
        Initialize soil surface properties.
        
        Args:
            temperature: Soil temperature (K)
            moisture: Volumetric soil moisture (m³/m³)
            sand: Sand fraction (0-1)
            clay: Clay fraction (0-1)
            diel_model: Dielectric model to use ('dobson', 'mironov', or 'wang')
            rms_hgt: Root mean square height (m), defaults to 0.01
            corr_length: Correlation length (m), defaults to 0.1
            bulk_density: Bulk density of soil (g/cm³), defaults to 1.3
            specific_density: Specific density of soil minerals (g/cm³), defaults to 2.65
        """
        # Validate input parameters
        if moisture < ZERO or moisture > ONE:
            raise ValueError(f"Soil moisture must be between {ZERO} and {ONE}")
        if sand < ZERO or sand > ONE:
            raise ValueError(f"Sand fraction must be between {ZERO} and {ONE}")
        if clay < ZERO or clay > ONE:
            raise ValueError(f"Clay fraction must be between {ZERO} and {ONE}")
        if sand + clay > ONE:
            raise ValueError("Sum of sand and clay fractions cannot exceed 1")
        if rms_hgt is not None and rms_hgt <= ZERO:
            raise ValueError("Root mean square height must be positive")
        if corr_length is not None and corr_length <= ZERO:
            raise ValueError("Correlation length must be positive")
        if temperature < ZERO:
            raise ValueError("Temperature must be positive")
        if bulk_density is not None and bulk_density <= ZERO:
            raise ValueError("Bulk density must be positive")
        if specific_density is not None and specific_density <= ZERO:
            raise ValueError("Specific density must be positive")
            
        self.temperature = temperature
        self.moisture = moisture
        self.sand = sand
        self.clay = clay
        self.diel_model = diel_model
        self.rms_hgt = rms_hgt if rms_hgt is not None else DEFAULT_RMS_HGT
        self.corr_length = corr_length if corr_length is not None else DEFAULT_CORR_LENGTH
        self.bulk_density = bulk_density if bulk_density is not None else DEFAULT_SOIL_BULK_DENSITY
        self.specific_density = specific_density if specific_density is not None else DEFAULT_SOIL_SPECIFIC_DENSITY
        
    @property
    def silt(self) -> float:
        """Silt fraction (0-1)"""
        return ONE - self.sand - self.clay
    
    def dielectric_constant(self, sensor: Sensor) -> complex:
        """
        Calculate the complex dielectric constant of the soil.
        
        Args:
            sensor: Sensor object containing the operating frequency
            
        Returns:
            complex: Complex dielectric constant
        """
        diel_const_func = SoilDiels.get_model(self.diel_model)
        if diel_const_func is None:
            raise ValueError(f"Unknown dielectric model: {self.diel_model}")
        return diel_const_func(self, sensor.frequency)
    
    def __str__(self) -> str:
        """String representation of the Soil object."""
        return (
            f"Soil(temperature={self.temperature:.2f}K, "
            f"rms_hgt={self.rms_hgt:.3f}m, "
            f"corr_length={self.corr_length:.3f}m, "
            f"moisture={self.moisture:.3f}, "
            f"sand={self.sand:.3f}, "
            f"clay={self.clay:.3f}, "
            f"silt={self.silt:.3f}, "
            f"diel_model='{self.diel_model}')"
        ) 