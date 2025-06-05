"""
Effective dielectric models module for CanORT (Canopy Optical Radiative Transfer) model.
This module provides dielectric constant calculations for vegetation using different mixing models.

The effective permittivity is calculated using a mixing model that accounts for:
1. The dielectric constant of the leaf material
2. The volume fraction of leaves in the layer
3. The air gaps between leaves
"""

from typing import Callable, Dict, Literal, Protocol, runtime_checkable, Optional
from ..core.constants import *

@runtime_checkable
class LayerLike(Protocol):
    """Protocol defining the interface for leaf-like objects."""
    leaf_type: Literal['needle', 'sphere', 'disk']
    leaf_volumetric_fraction: float
    dielectric_constant: Callable[[float], complex]
    

class EffectivePermittivityModels:
    """A class containing different leaf dielectric models."""

    @staticmethod
    def power_law_mixing(
        layer: LayerLike,
        frequency: float,
        beta: Optional[float] = 0.5,
        es_external: Optional[float] = AIR_DIELECTRIC,
    ) -> complex:
        """Simple linear mixing model for leaf dielectric constant.
        
        reference:
            Kerr and Wigneron, 1994, Vegetation models and observations A review, 
            in Passive Microwave Remote Sensing of Land-Atmosphere Interactions, 1993, p317-344

            also refer to: 
                - Chapter 4.2.2, Aleksandr A. Čuchlancev, 2006. Microwave Radiometry of Vegetation Canopies
                - Chapter 5.5.5 Christian Mätzler, 2006, Thermal Microwave Radiation: Applications for Remote Sensing

        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties
            frequency: Operating frequency in GHz
            beta: Volume parameter of the inclusion phase, default is 0.5:
                - β=1 (the linear model), 
                - β=0.5 ( the refractive model)
                - β=0.33 (the cubic model)

            es_external: External dielectric constant, default is air dielectric constant
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        leaf_diel = layer.dielectric_constant(frequency)
        
        f=layer.leaf_volumetric_fraction

        # Calculate leaf dielectric constant using linear mixing
        es_eff = (es_external+f*(leaf_diel**beta-es_external))**(1/beta)
        
        return es_eff
    
    @staticmethod
    def maxwell_garnett(
        layer: LayerLike,
        frequency: float,
        es_external: Optional[float] = AIR_DIELECTRIC,
    ) -> complex:
        """Maxwell-Garnett mixing model for leaf dielectric constant.
        
        reference: 
            Matzler, 2006, Thermal Microwave Radiation: Applications for Remote Sensing
            p5.5.3 Clausius-Mossotti and Maxwell Garnett formula
        
        Note:
            for dilute mixtures (f << 1), all three mixing rules, Maxwell Garnett, Polder-Van Santen and coherent potential, predict the same results.
            typically f for leaves is 0.001-0.005

        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties, leaf as inclusion
            frequency: Operating frequency in GHz
            es_external: External dielectric constant, default is air dielectric constant
            
        Returns:
            complex: Complex dielectric constant
        """
        # calculate leaf volumetric fraction occupied
        f = layer.leaf_volumetric_fraction
        es_inclusion = layer.dielectric_constant(frequency)

        # Calculate leaf dielectric constant using Maxwell-Garnett mixing
        denominator=es_inclusion + 2 * es_external - f * (es_inclusion - es_external)

        es_eff = es_external + 3 * f * es_external * (es_inclusion - es_external) / denominator
        
        return es_eff

    # @staticmethod
    # def maxwell_garnett_mixed_phases(
    #     layer: LayerLike,
    #     frequency: float,
    #     es_external: Optional[float] = AIR_DIELECTRIC,
    # ) -> complex:
    #     """Maxwell-Garnett mixing model for leaf dielectric constant with mixed phases.
        
    #     reference: 
    #         Matzler, 2006, Thermal Microwave Radiation: Applications for Remote Sensing
    #         p5.5.3 Clausius-Mossotti and Maxwell Garnett formula

    #     TODO: implement this model for the presence of :
    #             - Dew and snow gannuals intercepted by the leaves
    #             - Complex leaf types (e.g. needles, spheres, disks)
    #     """
        
    #     pass

    
    @staticmethod
    def nonspheric_model(
        layer: LayerLike,
        frequency: float,
        es_external: Optional[float] = AIR_DIELECTRIC,
    ) -> complex:
        """
        
        Args:
            leaf: Leaf-like object containing water content, temperature, and density properties
            frequency: Operating frequency in GHz
            es_external: External dielectric constant, default is air dielectric constant
        Returns:
            complex: Complex dielectric constant
        """
        # Calculate water dielectric constant
        leaf_diel = layer.dielectric_constant(frequency)
        
        # Calculate leaf dielectric constant using Bruggeman mixing
        f = layer.leaf_volumetric_fraction

        a=1/3. if layer.leaf_type == 'disk' else 2/3.

        es_eff = es_external + f * a * (leaf_diel - es_external)
        
        return es_eff
    
    @classmethod
    def get_model(cls, model_name: Literal["power_law", "spheric", "nonspheric"]) -> Callable:
        """Get the specified dielectric model function.
        
        Args:
            model_name: Name of the dielectric model to use
            
        Returns:
            Callable: The requested dielectric model function
            
        Raises:
            ValueError: If the model name is not recognized
        """
        models: Dict[str, Callable] = {
            "power_law": cls.power_law_mixing,
            "spheric": cls.maxwell_garnett,
            "nonspheric": cls.nonspheric_model
        }
        
        if model_name not in models:
            raise ValueError(f"Unknown dielectric model: {model_name}")
            
        return models[model_name] 