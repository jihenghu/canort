"""
Water dielectric models for CanORT.
This module provides models for calculating water dielectric constants.
"""

import numpy as np

class WaterDiels:
    """Collection of water dielectric constant models."""
    
    @staticmethod
    def debye(frequency: float, temperature: float) -> complex:
        """
        Calculate dielectric constant of water using Debye model. e single-Debye dielectric model P4.1, Ulaby & Long et al. (2014)
        
        Args:
            frequency: Frequency in GHz
            temperature: Temperature in Kelvin
            
        Returns:
            Complex dielectric constant of water
        """

        oC = temperature - 273.15

        # Static dielectric constant of water Klein and Swift (1977)
        es = 88.045 - 0.4147 * oC + 6.295e-4 * oC**2 + 1.075e-5 * oC**3
        
        # High frequency limit # Lane and Saxton (1952)
        einf = 4.9 
        
        # Relaxation time # Stogryn (1971)
        tau = 1.1109e-10 - 3.824e-12 * oC + 6.938e-14 * oC**2 - 5.096e-16 * oC**3 

        # Calculate real and imaginary parts
        omega = 2 * np.pi * frequency * 1e9
        e_real = einf + (es - einf) / (1 + (omega * tau)**2)
        e_imag = (es - einf) * omega * tau / (1 + (omega * tau)**2)
        
        return complex(e_real, e_imag) 