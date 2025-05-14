"""
Vegetation canopy modeling module for CanoRT.
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
from copy import deepcopy

from .layer import Layer


class Canopy:
    """A vegetation canopy composed of multiple layers."""
    
    def __init__(self, 
                 layers: Optional[List[Layer]] = None):
        """
        Initialize a vegetation canopy model.
        
        Args:
            layers: List of Layer objects, ordered from bottom to top
        """
        self.layers = layers if layers is not None else []

    @property
    def nlayers(self) -> int:
        """number of layers"""
        return len(self.layers)
    
    @property
    def thickness(self) -> float:
        """total thickness of the canopy"""
        return sum(layer.thickness for layer in self.layers)
    
    @property
    def layer_thicknesses(self) -> np.ndarray:
        """thicknesses of the layers"""
        return np.array([layer.thickness for layer in self.layers])
    
    @property
    def layer_top_heights(self) -> np.ndarray:
        """Get the height of the top of each layer, ordered from bottom to top."""
        return np.cumsum(self.layer_thicknesses)
    
    @property
    def z(self) -> np.ndarray:
        """height of each interface, that is, 0 and the heights of the top of each layer"""
        return np.insert(self.layer_top_heights, 0, 0)

    @property
    def layer_bottom_heights(self) -> np.ndarray:
        """height of the bottom of each layer, i.e., 0 to the n-1 layer"""
        return self.z[:-1]
    
    @property
    def layer_middle_heights(self) -> np.ndarray:
        """height of the middle of each layer, i.e., the average of the top and bottom heights"""
        return (self.layer_top_heights + self.layer_bottom_heights) / 2
    
    @property
    def layer_lais(self) -> np.ndarray:
        """leaf area index of each layer"""
        return np.array([layer.lai for layer in self.layers])
    
    @property
    def LAI(self) -> float:
        """total leaf area of the canopy"""
        return sum(layer.lai for layer in self.layers)
    
    @property
    def layer_temperatures(self) -> np.ndarray:
        """temperature of each layer"""
        return np.array([layer.temperature for layer in self.layers])
    
    @property
    def layer_leaf_moisture_content(self) -> np.ndarray:
        """leaf volumetric moisture content of each layer in m3/m3"""
        return np.array([layer.water_volumetric_fraction for layer in self.layers])
    
    @property
    def total_agb(self) -> float:
        """above ground biomass in kg/m²"""
        return sum(layer.agb for layer in self.layers)
    
    @property
    def total_vwc(self) -> float:
        """total water content in kg/m²"""
        return sum(layer.layer_water_content for layer in self.layers)
    
    @property
    def mean_lfmc(self) -> float:
        """mean live fuel moisture content in kg/kg"""
        return self.total_vwc / self.total_agb

    def append_layer(self, layer: Layer) -> None:
        """
        Add a new layer to the top of the canopy.
        
        Note:
            Layers are added to the top of the canopy (highest position).
        """
        self.layers.append(layer)

    def delete_layer(self, ilayer: int) -> None:
        """Delete a layer
        
        Args:
            ilayer: index of the layer to delete
        """
        self.layers.pop(ilayer)

    def update_layer_number(self, n_layers: int) -> None:
        """
        Update the number of layers in the canopy.
        If n_layers > current number of layers, new layers are added with default properties.
        If n_layers < current number of layers, layers are removed from the top.
        
        Note:
            When removing layers, they are removed from the top down.
            When adding layers, they are added to the top.
        
        Args:
            n_layers: Desired number of layers
        """
        current_layers = len(self.layers)
        
        if n_layers > current_layers:
            # Add new layers
            for _ in range(n_layers - current_layers):
                self.append_layer(Layer(
                    thickness=1.0,
                    temperature=300.0
                ))
        elif n_layers < current_layers:
            # Remove layers from the top
            self.layers = self.layers[:n_layers]
    
    def __add__(self, other: 'Canopy') -> 'Canopy':
        """
        Combine two canopies by stacking them.
        The other canopy is placed on top of this canopy.
        
        Note:
            The resulting canopy maintains bottom-to-top ordering of layers.
        
        Args:
            other: Another Canopy object to stack on top
            
        Returns:
            A new Canopy object combining both canopies
        """
        # Create a deep copy of this canopy
        new_canopy = deepcopy(self)
        
        # Add layers from the other canopy
        for layer in other.layers:
            new_canopy.append_layer(deepcopy(layer))
        
        return new_canopy
    
    def __deepcopy__(self, memo) -> 'Canopy':
        """
        Create a deep copy of the canopy.
        
        Note:
            The copied canopy maintains the same bottom-to-top layer ordering.
        
        Args:
            memo: Dictionary used by deepcopy to track objects
            
        Returns:
            A deep copy of the Canopy object
        """
        # Create a new canopy with deep copies of all components
        return Canopy(
            layers=[deepcopy(layer) for layer in self.layers]
        )

    def __str__(self) -> str:
        """String representation of the Canopy object."""
        info = [
            "Description: A sample canopy object",
            f"Number of layers: {self.nlayers}",
            f"Total LAI: {self.LAI:.2f}",
            f"Total thickness: {self.thickness:.2f}m",
            f"Total AGB: {self.total_agb:.2f}kg/m²",
            f"Total VWC: {self.total_vwc:.2f}kg/m²",
            f"Mean LFMC: {self.mean_lfmc:.2f}kg/kg",
            "\nLayer Details:"
        ]
        
        for i, layer in enumerate(self.layers):
            info.append(f"\nLayer {i+1}:")
            info.append(f"  BottomHeight: {self.layer_bottom_heights[i]:.2f} m")
            info.append(f"  Thickness: {layer.thickness:.2f} m")
            info.append(f"  LAI: {layer.lai:.2f} m²/m²")
            info.append(f"  Leaf Thickness: {layer.leaf_thickness:.3f} mm")
            info.append(f"  Temperature: {layer.temperature:.2f} K")
            info.append(f"  Water Volumetric Fraction: {layer.water_volumetric_fraction:.3f} m3/m3")
            info.append(f"  Dry Mass Density: {layer.dry_mass_density:.3f} g/cm³")
            info.append(f"  Layer Water Content: {layer.layer_water_content:.2f} kg/m²")
            info.append(f"  Live Fuel Moisture Content: {layer.lfmc:.2f} kg/kg")
            info.append(f"  Above Ground Biomass: {layer.agb:.2f} kg/m²")
        
        return "\n".join(info) 