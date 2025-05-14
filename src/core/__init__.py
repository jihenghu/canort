"""
Core module for CanORT (Canopy Optical Radiative Transfer) model.
This package contains the fundamental classes for canopy modeling.
"""

from .layer import Layer
from .canopy import Canopy

__all__ = ['Layer', 'Canopy'] 