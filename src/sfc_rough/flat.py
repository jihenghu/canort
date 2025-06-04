"""
Flat surface model for CanORT.
This module provides the flat surface scattering model.
"""

import numpy as np
from typing import Protocol, runtime_checkable

@runtime_checkable
class SoilLike(Protocol):
    """Protocol defining the interface for soil-like objects."""
    rms_hgt: float
    corr_length: float

def flat_model(
    soil: SoilLike,
    k: float,
    theta: float,
    eps: complex
) -> tuple[float, float, float, float]:
    """
    Calculate flat surface scattering coefficients.
    
    Args:
        soil: Soil-like object containing rms_hgt and corr_length
        k: Wavenumber (2π/λ)
        theta: Incidence angle in radians
        eps: Complex dielectric constant
        
    Returns:
        tuple: (R_hh, R_vv, T_hh, T_vv) where:
            R_hh: Horizontal-horizontal reflection coefficient
            R_vv: Vertical-vertical reflection coefficient
            T_hh: Horizontal-horizontal transmission coefficient
            T_vv: Vertical-vertical transmission coefficient
    """
    # For flat surface, roughness factor is 1
    return 1.0, 1.0, 1.0, 1.0 