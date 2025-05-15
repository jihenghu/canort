"""
Constants module for CanORT (Canopy Optical Radiative Transfer) model.
This module defines physical and mathematical constants used throughout the project.
"""

import numpy as np

# Physical constants
SPEED_OF_LIGHT = 299792458.0  # Speed of light in vacuum (m/s)
PLANCK_CONSTANT = 6.62607015e-34  # Planck constant (J⋅s)
BOLTZMANN_CONSTANT = 1.380649e-23  # Boltzmann constant (J/K)
STEFAN_BOLTZMANN = 5.670374419e-8  # Stefan-Boltzmann constant (W⋅m⁻²⋅K⁻⁴)
AVOGADRO_NUMBER = 6.02214076e23  # Avogadro constant (mol⁻¹)
GAS_CONSTANT = 8.31446261815324  # Gas constant (J⋅mol⁻¹⋅K⁻¹)

# Water properties
WATER_DENSITY_KG_M3 = 1000.0  # Water density at 20°C (kg/m³)
WATER_DENSITY_G_CM3 = 1.0  # Water density at 20°C (g/cm³)
WATER_MOLECULAR_WEIGHT = 18.01528  # Water molecular weight (g/mol)
WATER_VAPOR_DENSITY = 0.0173  # Water vapor density at 20°C (kg/m³)
WATER_SPECIFIC_HEAT = 4186.0  # Water specific heat capacity (J/kg·K)
WATER_LATENT_HEAT = 2.257e6  # Water latent heat of vaporization at 20°C (J/kg)

# Mathematical constants
PI = np.pi  # Pi (π)
E = np.e  # Euler's number (e)
ZERO = 0.0
ONE = 1.0
TWO = 2.0
THOUSAND = 1e3
GHz = 1e9

# Default values for canopy parameters
DEFAULT_LEAF_THICKNESS = 0.17  # Default leaf thickness (mm)
DEFAULT_DRY_MASS_DENSITY = 0.3  # Default dry mass density (g/cm³)
DEFAULT_WATER_VOLUMETRIC_FRACTION = 0.0  # Default water volumetric fraction (m3/m3)
DEFAULT_LAI = 0.0  # Default leaf area index (m²/m²)
DEFAULT_TEMPERATURE = 293.15  # Default temperature (K) - 20°C

# Default values for soil parameters
DEFAULT_SOIL_BULK_DENSITY = 1.3  # Default soil bulk density (g/cm³)
DEFAULT_SOIL_SPECIFIC_DENSITY = 2.65  # Default soil specific density (g/cm³)
DEFAULT_RMS_HGT = 0.01  # Default root mean square height (m)
DEFAULT_CORR_LENGTH = 0.1  # Default correlation length (m)
DEFAULT_SOIL_MOISTURE = 0.2  # Default soil moisture (m³/m³)
DEFAULT_SAND_FRACTION = 0.5  # Default sand fraction
DEFAULT_CLAY_FRACTION = 0.2  # Default clay fraction

# Unit conversion factors
MM_TO_M = 1e-3  # Millimeters to meters
CM_TO_M = 1e-2  # Centimeters to meters
G_TO_KG = 1e-3  # Grams to kilograms
CM3_TO_M3 = 1e-6  # Cubic centimeters to cubic meters
K2KG = 1e-3  # Kilograms to grams

# Dielectric constants
WATER_DIELECTRIC = 80.0 + 0j  # Complex dielectric constant of water at 20°C
AIR_DIELECTRIC = 1.0 + 0j  # Complex dielectric constant of air

# Wavelength ranges (in meters)
VISIBLE_RANGE = (380e-9, 750e-9)  # Visible light range
NIR_RANGE = (750e-9, 1400e-9)  # Near-infrared range
SWIR_RANGE = (1400e-9, 3000e-9)  # Short-wave infrared range
TIR_RANGE = (3000e-9, 14000e-9)  # Thermal infrared range

# Atmospheric parameters
STANDARD_PRESSURE = 101325.0  # Standard atmospheric pressure (Pa)
STANDARD_TEMPERATURE = 288.15  # Standard temperature (K) - 15°C
STANDARD_HUMIDITY = 0.0  # Standard relative humidity (fraction)

# Canopy structure parameters
MIN_LAYER_THICKNESS = 0.01  # Minimum layer thickness (m)
MAX_LAYER_THICKNESS = 100.0  # Maximum layer thickness (m)
MIN_LAI = 0.0  # Minimum leaf area index (m²/m²)
MAX_LAI = 10.0  # Maximum leaf area index (m²/m²)
MIN_WATER_VOLUMETRIC_FRACTION = 0.0  # Minimum water volumetric fraction (m3/m3)
MAX_WATER_VOLUMETRIC_FRACTION = 1.0  # Maximum water volumetric fraction (m3/m3) 