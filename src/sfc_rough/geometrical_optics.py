"""
Geometrical Optics surface model for CanORT.
This module provides the Geometrical Optics surface scattering model.
"""

import numpy as np
from typing import Protocol, runtime_checkable

@runtime_checkable
class SoilLike(Protocol):
    """Protocol defining the interface for soil-like objects."""
    rms_hgt: float
    corr_length: float

def geometrical_optics_model(
    soil: SoilLike,
    k: float,
    theta: float,
    eps: complex
) -> tuple[float, float, float, float]:
    """
    Calculate Geometrical Optics surface scattering coefficients.
    
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
    # Calculate roughness parameters
    h = soil.rms_hgt
    l = soil.corr_length
    
    # Calculate surface parameters
    kz = k * np.cos(theta)
    kx = k * np.sin(theta)
    
    # Calculate roughness factor
    roughness = np.exp(-2 * kz**2 * h**2)
    
    # Calculate reflection coefficients
    R_hh = roughness
    R_vv = roughness
    
    # Calculate transmission coefficients
    T_hh = 1.0 - R_hh
    T_vv = 1.0 - R_vv
    
    return R_hh, R_vv, T_hh, T_vv 