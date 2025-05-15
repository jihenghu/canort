"""
Soil creation module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides functions to create soil instances with different configurations.
"""

from typing import Optional, Literal
from ..core.soil import Soil

def make_soil(
    temperature: float = 293.15,  # 20°C in Kelvin
    moisture: float = 0.2,  # 20% volumetric moisture
    sand: float = 0.5,  # 50% sand
    clay: float = 0.3,  # 30% clay
    rms_hgt: Optional[float] = None,  # Root mean square height in meters
    corr_length: Optional[float] = None,  # Correlation length in meters
    diel_model: Literal["dobson", "mironov", "wang"] = "dobson",
    bulk_density: Optional[float] = None,  # Bulk density in g/cm³
    specific_density: Optional[float] = None,  # Specific density in g/cm³
) -> Soil:
    """Create a soil instance with specified parameters.
    
    Args:
        temperature: Soil temperature in Kelvin. Default is 293.15 K (20°C).
        moisture: Volumetric soil moisture (0-1). Default is 0.2 (20%).
        sand: Sand fraction (0-1). Default is 0.5 (50%).
        clay: Clay fraction (0-1). Default is 0.3 (30%).
        rms_hgt: Root mean square height in meters. Optional.
        corr_length: Correlation length in meters. Optional.
        diel_model: Dielectric model to use. One of "dobson", "mironov", or "wang".
        bulk_density: Bulk density in g/cm³. Optional.
        specific_density: Specific density in g/cm³. Optional.
        
    Returns:
        Soil: Configured soil instance
    """
    return Soil(
        temperature=temperature,
        moisture=moisture,
        sand=sand,
        clay=clay,
        rms_hgt=rms_hgt,
        corr_length=corr_length,
        diel_model=diel_model,
        bulk_density=bulk_density,
        specific_density=specific_density
    )

def create_sandy_soil(
    temperature: float = 293.15,
    moisture: float = 0.15,
    rms_hgt: Optional[float] = None,
    corr_length: Optional[float] = None,
    diel_model: Literal["dobson", "mironov", "wang"] = "dobson",
) -> Soil:
    """Create a sandy soil instance (80% sand, 10% clay).
    
    Args:
        temperature: Soil temperature in Kelvin. Default is 293.15 K (20°C).
        moisture: Volumetric soil moisture (0-1). Default is 0.15 (15%).
        rms_hgt: Root mean square height in meters. Optional.
        corr_length: Correlation length in meters. Optional.
        diel_model: Dielectric model to use. One of "dobson", "mironov", or "wang".
        
    Returns:
        Soil: Configured sandy soil instance
    """
    return make_soil(
        temperature=temperature,
        moisture=moisture,
        sand=0.8,
        clay=0.1,
        rms_hgt=rms_hgt,
        corr_length=corr_length,
        diel_model=diel_model
    )

def create_clayey_soil(
    temperature: float = 293.15,
    moisture: float = 0.25,
    rms_hgt: Optional[float] = None,
    corr_length: Optional[float] = None,
    diel_model: Literal["dobson", "mironov", "wang"] = "dobson",
) -> Soil:
    """Create a clayey soil instance (20% sand, 60% clay).
    
    Args:
        temperature: Soil temperature in Kelvin. Default is 293.15 K (20°C).
        moisture: Volumetric soil moisture (0-1). Default is 0.25 (25%).
        rms_hgt: Root mean square height in meters. Optional.
        corr_length: Correlation length in meters. Optional.
        diel_model: Dielectric model to use. One of "dobson", "mironov", or "wang".
        
    Returns:
        Soil: Configured clayey soil instance
    """
    return make_soil(
        temperature=temperature,
        moisture=moisture,
        sand=0.2,
        clay=0.6,
        rms_hgt=rms_hgt,
        corr_length=corr_length,
        diel_model=diel_model
    )

def create_loamy_soil(
    temperature: float = 293.15,
    moisture: float = 0.2,
    rms_hgt: Optional[float] = None,
    corr_length: Optional[float] = None,
    diel_model: Literal["dobson", "mironov", "wang"] = "dobson",
) -> Soil:
    """Create a loamy soil instance (40% sand, 20% clay).
    
    Args:
        temperature: Soil temperature in Kelvin. Default is 293.15 K (20°C).
        moisture: Volumetric soil moisture (0-1). Default is 0.2 (20%).
        rms_hgt: Root mean square height in meters. Optional.
        corr_length: Correlation length in meters. Optional.
        diel_model: Dielectric model to use. One of "dobson", "mironov", or "wang".
        
    Returns:
        Soil: Configured loamy soil instance
    """
    return make_soil(
        temperature=temperature,
        moisture=moisture,
        sand=0.4,
        clay=0.2,
        rms_hgt=rms_hgt,
        corr_length=corr_length,
        diel_model=diel_model
    ) 