"""
Soil dielectric models module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides dielectric constant calculations for soil using different models.
"""

from typing import Callable, Dict, Literal, Protocol, runtime_checkable
import numpy as np
from .water_dielectrics import WaterDiels
import warnings


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
    def dobson85_model(
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
        # Soil specific parameters
        beta1 = 1.2748 - 0.519 * soil.sand - 0.152 * soil.clay
        beta2 = 1.33797 - 0.603 * soil.sand - 0.166 * soil.clay

        # effective conductivity σef
        sigma = -1.645 + 1.939*soil.bulk_density - 2.256*soil.sand + 1.594*soil.clay

        # Water dielectric constant
        eps_w = WaterDiels.debye(frequency, soil.temperature)
        
        # 2Πf*epsilon0
        eps0f = 2 * np.pi * frequency*1e9 * 8.854187817e-12

        # imaginary part of the water dielectric constant
        eps_w_imag = eps_w.imag + (soil.specific_density - soil.bulk_density)/ soil.specific_density / soil.moisture * sigma/ eps0f

        # empirical parameter
        alpha = 0.65

        # composite DC of the soil mineral contents
        eps1=(1.01+0.44*soil.specific_density)**2-0.062

        # Calculate real and imaginary parts
        e_real = (1 + soil.bulk_density/soil.specific_density*(eps1**alpha-1) + soil.moisture**beta1 * eps_w.real**alpha - soil.moisture)**(1/alpha)
        e_imag = (soil.moisture**beta2 * eps_w_imag**alpha)**(1/alpha)
        
        return complex(e_real, e_imag)
    
    
    @staticmethod
    def mironov04_model(
        soil: SoilLike,
        frequency: float
    ) -> complex:
        """Mironov et al. (2004) dielectric model. 
        adapted from the lis-cmem3/dielsoil_sub.F90 Patricia de Rosnay, October 9 2007,
        as adapted from the Matlab version of JP Wigneron.
        
        This is a detailed implementation of the Generalized Refractive Mixing Dielectric Model
        for moist soils, developed and validated from 1 to 10 GHz.
        
        Reference:
            Mironov et al: Generalized Refractive Mixing Dielectric Model for moist soil
            IEEE Trans. Geosc. Rem. Sens., vol 42 (4), 773-785. 2004.
        
        Args:
            soil: Soil-like object containing moisture and clay properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Convert frequency to Hz
        f = frequency * 1e9
        
        # Check frequency range validity
        if frequency > 10.0:
            warnings.warn("Mironov model is only validated for frequencies from 1 to 10 GHz", UserWarning)

        # Constants
        pi = np.pi
        eps_0 = 8.854e-12  # permittivity of free space
        eps_winf = 4.9     # dielectric constant at infinite frequency
        
        # RI & NAC of dry soils
        znd = 1.634 - 0.539 * soil.clay + 0.2748 * soil.clay**2
        zkd = 0.03952 - 0.04038 * soil.clay
        
        # Maximum bound water fraction
        zxmvt = 0.02863 + 0.30673 * soil.clay
        
        # Bound water parameters
        zep0b = 79.8 - 85.4 * soil.clay + 32.7 * soil.clay**2
        ztaub = 1.062e-11 + 3.450e-12 * soil.clay
        zsigmab = 0.3112 + 0.467 * soil.clay
        
        # Unbound (free) water parameters
        zep0u = 100.0
        ztauu = 8.5e-12
        zsigmau = 0.3631 + 1.217 * soil.clay
        
        # Computation of epsilon water (bound & unbound)
        zcxb = (zep0b - eps_winf) / (1. + (2.*pi*f*ztaub)**2)
        zepwbx = eps_winf + zcxb
        zepwby = zcxb * (2.*pi*f*ztaub) + zsigmab / (2.*pi*eps_0*f)
        
        zcxu = (zep0u - eps_winf) / (1. + (2.*pi*f*ztauu)**2)
        zepwux = eps_winf + zcxu
        zepwuy = zcxu * (2.*pi*f*ztauu) + zsigmau/(2.*pi*eps_0*f)
        
        # Computation of refractive index of water (bound & unbound)
        znb = np.sqrt(np.sqrt(zepwbx**2 + zepwby**2) + zepwbx) / np.sqrt(2)
        zkb = np.sqrt(np.sqrt(zepwbx**2 + zepwby**2) - zepwbx) / np.sqrt(2)
        
        znu = np.sqrt(np.sqrt(zepwux**2 + zepwuy**2) + zepwux) / np.sqrt(2)
        zku = np.sqrt(np.sqrt(zepwux**2 + zepwuy**2) - zepwux) / np.sqrt(2)
        
        # Computation of soil refractive index
        zxmvt2 = min(soil.moisture, zxmvt)
        zflag = 1.0 if soil.moisture >= zxmvt else 0.0
        
        znm = znd + (znb - 1.) * zxmvt2 + (znu - 1.) * (soil.moisture - zxmvt) * zflag
        zkm = zkd + zkb * zxmvt2 + zku * (soil.moisture - zxmvt) * zflag
        
        # Computation of soil dielectric constant
        zepmx = znm**2 - zkm**2
        zepmy = znm * zkm * 2
        
        return complex(zepmx, zepmy)
    
    @staticmethod
    def wang80_model(
        soil: SoilLike,
        frequency: float
    ) -> complex:
        """Wang and Schmugge (1980) dielectric model.
        
        Adapted from the Fortran implementation in lis-cmem3/dielsoil_sub.F90.
        Developed and validated for 1.4 and 5 GHz.
        
        Reference:
            Wang and Schmugge, 1980: An empirical model for the complex dielectric
            permittivity of soils as a function of water content.
            IEEE Trans. Geosci. Rem. Sens., GE-18, No. 4, 288-295.
            
        Args:
            soil: Soil-like object containing moisture, sand, clay, and bulk density properties
            frequency: Operating frequency in GHz
            
        Returns:
            complex: Complex dielectric constant
        """
        # Check frequency range validity
        if frequency > 5.0:
            warnings.warn("Wang and Schmugge (1980) soil dielectric model is only validated for frequencies up to 5 GHz", UserWarning)
            
        # Get water dielectric constant
        eps_w = WaterDiels.debye(frequency, soil.temperature)
        
        # Dielectric constants of components
        eps_i = complex(3.2, 0.1)  # ice
        eps_a = complex(1.0, 0.0)  # air
        eps_r = complex(5.5, 0.2)  # rock
        
        # Calculate wilting point
        wp = 0.06774 - 0.064 * soil.sand + 0.478 * soil.clay
        
        # Calculate alpha parameter based on frequency
        if frequency > 2.5:
            alpha = 0.0
        else:
            alpha = min(100.0 * wp, 26.0)
            
        # Calculate gamma parameter
        gamma = -0.57 * wp + 0.481
        
        # Calculate transition moisture point
        wt = 0.49 * wp + 0.165
        
        # Calculate porosity if not provided
        porosity = 1.0 - soil.bulk_density/soil.specific_density
        
        # Calculate dielectric constant of soil-water mixture
        if soil.moisture <= wt:
            # Bound water region
            eps_x = eps_i + (eps_w - eps_i) * (soil.moisture/wt) * gamma
            eps = soil.moisture * eps_x + (porosity - soil.moisture) * eps_a + (1.0 - porosity) * eps_r
        else:
            # Free water region
            eps_x = eps_i + (eps_w - eps_i) * gamma
            eps = wt * eps_x + (soil.moisture - wt) * eps_w + (porosity - soil.moisture) * eps_a + (1.0 - porosity) * eps_r
            
        # Add conductivity loss
        eps_cl = complex(0.0, alpha * soil.moisture**2)
        eps = eps + eps_cl
        
        return eps
    
    @classmethod
    def get_model(cls, model_name: Literal["dobson85", "mironov04", "wang80"]) -> Callable:
        """Get the specified dielectric model function.
        
        Args:
            model_name: Name of the dielectric model to use
            
        Returns:
            Callable: The requested dielectric model function
            
        Raises:
            ValueError: If the model name is not recognized
        """
        models: Dict[str, Callable] = {
            "dobson85": cls.dobson85_model,
            "mironov04": cls.mironov04_model,
            "wang80": cls.wang80_model
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown dielectric model: {model_name}, must be one of {list(models.keys())}")
            
        return models[model_name] 