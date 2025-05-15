# coding: utf-8

"""
Sensor module for CanORT (Canopy Optical Radiative Transfer) model.
This module defines the Sensor class which represents the passive microwave remote sensing instrument.
"""

from typing import Optional, List, Union
import numpy as np
from .constants import *

def passive(frequency: Union[float, List[float]], 
           theta: Union[float, List[float]], 
           polarization: Optional[List[str]] = None,
           name: Optional[str] = None) -> 'Sensor':
    """Create a configuration for passive microwave sensor.
    
    Args:
        frequency: Operating frequency in GHz
        theta: Viewing angle in degrees from vertical
        polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
        name: Name of the sensor
        
    Returns:
        Sensor: Configured sensor instance
    """
    if polarization is None:
        polarization = ["V", "H"]
        
    sensor = Sensor(frequency, theta, polarization, name)
    sensor.basic_checks()
    return sensor

class Sensor:
    """A class representing a passive microwave remote sensing instrument."""
    
    def __init__(self,
                 frequency: Union[float, List[float]] = 1.4,  # Default frequency in GHz
                 theta: Union[float, List[float]] = 0.0,  # Viewing angle in degrees from vertical
                 polarization: Optional[List[str]] = None,  # List of polarizations (H and/or V)
                 name: Optional[str] = None):
        """
        Initialize sensor properties.
        
        Args:
            frequency: Operating frequency in GHz
            theta: Viewing angle in degrees from vertical
            polarization: List of polarizations ('H' and/or 'V'). Defaults to both.
            name: Name of the sensor
        """
        # Convert frequency to numpy array and validate
        self.frequency = np.asarray(frequency).squeeze() if isinstance(frequency, (list, tuple)) else frequency
        if np.any(self.frequency <= ZERO):
            raise ValueError("Frequency must be positive")
            
        # Convert theta to numpy array and validate
        self.theta_deg = np.asarray(theta).squeeze() if isinstance(theta, (list, tuple)) else theta
        if np.any(self.theta_deg < ZERO) or np.any(self.theta_deg > 90):
            raise ValueError("Viewing angle must be between 0 and 90 degrees")
            
        # Set polarization
        if polarization is None:
            polarization = ["V", "H"]
        elif isinstance(polarization, str):
            polarization = list(polarization)
        self.polarization = polarization
        
        # Set name
        self.name = name
        
        # Convert angles to radians for internal calculations
        self.theta = np.radians(self.theta_deg)
        self.mu = np.cos(self.theta)  # Cosine of viewing angle
        
        # Calculate wavelength
        self.wavelength = SPEED_OF_LIGHT / (self.frequency * GHz)
        
    @property
    def wavenumber(self) -> float:
        """Wave number in m⁻¹"""
        return 2 * np.pi / self.wavelength
    
    def basic_checks(self):
        """Perform basic validation checks on sensor parameters."""
        # Check frequency range (below 300 MHz is an indication the units may be wrong)
        frequency_min = np.min(np.atleast_1d(self.frequency))
        if frequency_min < 0.3:  # 300 MHz in GHz
            raise ValueError("Frequency not in microwave range: check units are GHz")
    
    def __str__(self) -> str:
        """String representation of the Sensor object."""
        return (
            f"Sensor(frequency={self.frequency:.2f}GHz, "
            f"theta={self.theta_deg:.1f}°, "
            f"polarization={self.polarization}"
            + (f", name='{self.name}'" if self.name else "")
            + ")"
        ) 