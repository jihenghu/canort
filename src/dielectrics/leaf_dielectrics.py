"""
Leaf dielectric models module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides leaf-specific dielectric constant calculations and properties.
"""

from typing import Protocol, runtime_checkable, Dict, Callable, Literal
import numpy as np
from .effective_dielectrics import EffectivePermittivityModels, LeafLike
from ..core.constants import *
import warnings

@runtime_checkable
class LeafLike(Protocol):
    """Protocol defining the interface for leaf properties.
    
    Attributes:
        water_volumetric_fraction: Volume fraction of water in the leaf (m³/m³)
        water_gravimetric_fraction: Mass fraction of water in the leaf (kg/kg)
        temperature: Temperature in Kelvin

    """
    water_volumetric_fraction: float
    water_gravimetric_fraction: float
    temperature: float



class LeafDiels:
    """A class containing leaf-specific dielectric calculations and properties."""

    @staticmethod
    def ulaby_el_rayes_1987(
        leaf: LeafLike,
        frequency: float
    ) -> complex:
        """Ulaby and El Rayes (1987) dielectric model. 

        Reference:
            ULABY, F. T., and EL RAYES: Microwave dielectric spectrum of vegetation Part II: Dual-Dispersion Model, IEEE Trans. Geosci. Remote Sens., 1987, GE-25, pp. 550-7
        
        Description (from the chapter 5.7.4 of matzler (2006)):
            Ulaby and El Rayes (1987) assumed linear, empirical relationships between the dielectric constants and volume fractions of the vegetation components, free water, bound water, and a residual component due to organic matter and air. Their data were based on dielectric measurements of sucrose solution to determine the spectral behaviour of bound water and of drying corn leaves made with open-ended coaxial probes at frequencies up to 20 GHz (El Rayes and Ulaby, 1987a,b). As the probes are suitable for liquids, the results on sucrose were promising. Increased errors were found for leaves due to contact problems, limiting the measurements to frequencies smaller than 10 GHz. In addition, measurements with high water content were missing.

        Args:
            leaf: Leaf-like object containing water volumetric fraction, temperature, dry mass density, thickness and area
            frequency: Operating frequency in GHz

        Returns:
            complex: Complex dielectric constant
        """

        if frequency > 20.0:
            warnings.warn("Ulaby and El Rayes (1987) dielectric model is only validated for frequencies below 20 GHz", UserWarning)

        if leaf.water_volumetric_fraction > 0.5:
            warnings.warn("Ulaby and El Rayes (1987) dielectric model may not be accurate for high water content > 0.5 m3/m3", UserWarning)

        # simplified model from Ulaby and Long (2014), chapter 4.9  
          


        # Calculate volume fractions of free and bound water
        # mg= leaf.water_gravimetric_fraction
        # er = 1.7 - 0.74 * mg + 6.16 * mg**2
        # vfw = mg * (0.55 * mg + 0.76) 
        # vbw = 4.64 * mg**2 / (1 + 7.36 * mg**2)

        
        # Calculate volume fractions of free and bound water (eq20-22 of Ulaby and El Rayes (1987))
        # Get volume moisture content from leaf properties
        vmc = leaf.water_volumetric_fraction
        er = 1.7 + 3.2 * vmc + 6.5 * vmc**2
        vfw = vmc * (0.82 * vmc + 0.166) 
        vbw = 31.4 * vmc**2 / (1 + 59.5 * vmc**2)

        # Calculate free water dielectric constant
        efw_real = 4.9 + 74.4 / (1 + (frequency/18.)**2)
        efw_imag = 74.4 * frequency / 18. / (1 + (frequency/18.)**2)
        
        # Calculate bound water dielectric constant
        ebw_real = 2.9 + 55 * (1 + np.sqrt(frequency/0.36)) / ((1 + np.sqrt(frequency/0.36))**2 + (frequency/0.36))
        ebw_imag = 55 * np.sqrt(frequency/0.36) / ((1 + np.sqrt(frequency/0.36))**2 + (frequency/0.36))

        # Calculate complex dielectric constant
        ev_real = er + efw_real * vfw + ebw_real * vbw
        ev_imag = efw_imag * vfw + ebw_imag * vbw
        
        return complex(ev_real, ev_imag)

    @staticmethod
    def matzler1994(
        leaf: LeafLike,
        frequency: float
    ) -> complex:
        """Matzler (1994) dielectric model. 
        Combined the data of Ulaby and El Rayes (1987), El Rayes and Ulaby (1987b) and of Mätzler and Sume (1989) to derive a dielectric formula for vegetation over the frequency range from 1 to 100 GHz.

        Reference:
            MÄTZLER, C.: Microwave (1-100 GHz) dielectric model of leaves, 
            IEEE Trans. Geosci. Remote Sens., 1994, 32(4), pp. 947-952

        Args:
            leaf: Leaf-like object containing water volumetric fraction, temperature, dry mass density, thickness and area
            frequency: Operating frequency in GHz

        Returns:
            complex: Complex dielectric constant
        """
        # gravimetric dry mass fraction (on a fresh-mass basis) 
        Md = 1 - leaf.water_gravimetric_fraction  # on a dry-mass basis

        # permittivity of saline water at 20°C with 1% salinity:  Ulaby and El Rayes (1987)
        S=10 # 1% salinity
        sigma=0.17*S-0.0013*S**2

        esw_real = 4.9 + 74.4 / (1 + (frequency/18.)**2)
        esw_imag = 74.4 * frequency / 18. / (1 + (frequency/18.)**2)+ 18*sigma /frequency

        es=0.51+3.84*Md+0.522*(1-1.32*Md)*complex(esw_real,esw_imag)

        return es
 
    @classmethod
    def get_model(cls, model_name: Literal["ulaby87", "matzler94"]) -> Callable:
        """Get the specified dielectric model function.
        
        Args:
            model_name: Name of the dielectric model to use
            
        Returns:
            Callable: The requested dielectric model function
            
        Raises:
            ValueError: If the model name is not recognized
        """
        models: Dict[str, Callable] = {
            "ulaby87": cls.ulaby_el_rayes_1987,
            "matzler94": cls.matzler1994
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown dielectric model: {model_name}, must be one of {list(models.keys())}")
            
        return models[model_name]
 

