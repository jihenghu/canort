"""
Dielectric models for CanORT.
This package provides dielectric constant models for various materials.
"""

from .water_dielectrics import WaterDiels
from .soil_dielectrics import SoilDiels

__all__ = ['WaterDiels', 'SoilDiels'] 