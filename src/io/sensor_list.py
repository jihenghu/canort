"""
Sensor list module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides configurations for common passive microwave sensors.
"""

from typing import Optional, List, Union
from ..core.sensor import passive, Sensor

def amsre(frequency: Optional[Union[float, List[float]]] = None,
          theta: float = 55.0,
          polarization: Optional[List[str]] = None) -> Sensor:
    """AMSR-E (Advanced Microwave Scanning Radiometer for EOS) sensor configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses all AMSR-E frequencies.
        theta: Viewing angle in degrees from vertical. Default is 55°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured AMSR-E sensor instance
    """
    if frequency is None:
        frequency = [6.925, 10.65, 18.7, 23.8, 36.5, 89.0]  # AMSR-E frequencies in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="AMSR-E")

def smap(frequency: Optional[Union[float, List[float]]] = None,
         theta: float = 40.0,
         polarization: Optional[List[str]] = None) -> Sensor:
    """SMAP (Soil Moisture Active Passive) radiometer configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses SMAP frequency.
        theta: Viewing angle in degrees from vertical. Default is 40°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured SMAP sensor instance
    """
    if frequency is None:
        frequency = 1.41  # SMAP L-band frequency in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="SMAP")

def smos(frequency: Optional[Union[float, List[float]]] = None,
         theta: float = 42.5,
         polarization: Optional[List[str]] = None) -> Sensor:
    """SMOS (Soil Moisture and Ocean Salinity) sensor configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses SMOS frequency.
        theta: Viewing angle in degrees from vertical. Default is 42.5°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured SMOS sensor instance
    """
    if frequency is None:
        frequency = 1.4  # SMOS L-band frequency in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="SMOS")

def gmi(frequency: Optional[Union[float, List[float]]] = None,
        theta: float = 52.8,
        polarization: Optional[List[str]] = None) -> Sensor:
    """GMI (Global Precipitation Measurement Microwave Imager) sensor configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses all GMI frequencies.
        theta: Viewing angle in degrees from vertical. Default is 52.8°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured GMI sensor instance
    """
    if frequency is None:
        frequency = [10.65, 18.7, 23.8, 36.5, 89.0, 166.0, 183.31]  # GMI frequencies in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="GMI")

def ssmis(frequency: Optional[Union[float, List[float]]] = None,
          theta: float = 53.1,
          polarization: Optional[List[str]] = None) -> Sensor:
    """SSMIS (Special Sensor Microwave Imager/Sounder) sensor configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses all SSMIS frequencies.
        theta: Viewing angle in degrees from vertical. Default is 53.1°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured SSMIS sensor instance
    """
    if frequency is None:
        frequency = [19.35, 22.235, 37.0, 91.655, 150.0, 183.31]  # SSMIS frequencies in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="SSMIS")

def amsr2(frequency: Optional[Union[float, List[float]]] = None,
          theta: float = 55.0,
          polarization: Optional[List[str]] = None) -> Sensor:
    """AMSR2 (Advanced Microwave Scanning Radiometer 2) sensor configuration.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses all AMSR2 frequencies.
        theta: Viewing angle in degrees from vertical. Default is 55°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured AMSR2 sensor instance
    """
    if frequency is None:
        frequency = [6.925, 7.3, 10.65, 18.7, 23.8, 36.5, 89.0]  # AMSR2 frequencies in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="AMSR2")

def mwri(frequency: Optional[Union[float, List[float]]] = None,
         theta: float = 55.0,
         polarization: Optional[List[str]] = None) -> Sensor:
    """MWRI (Microwave Radiation Imager) sensor configuration.
    
    MWRI is a passive microwave radiometer onboard the FengYun-3 satellites.
    It has 10 channels at 5 frequencies with dual polarization.
    
    Args:
        frequency: Operating frequency in GHz. If None, uses all MWRI frequencies.
        theta: Viewing angle in degrees from vertical. Default is 55°.
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        
    Returns:
        Sensor: Configured MWRI sensor instance
    """
    if frequency is None:
        frequency = [10.65, 18.7, 23.8, 36.5, 89.0]  # MWRI frequencies in GHz
        
    return passive(frequency=frequency, 
                  theta=theta, 
                  polarization=polarization,
                  name="MWRI") 