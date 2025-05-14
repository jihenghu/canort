# CanoRT (Microwave Radiative Transfer of Layered Vegetation Canopy)

A Python package for modeling microwave radiometry over layered vegetated scenario.

## Installation

### Option 1: Install from source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/canort.git
cd canort
```

2. Create and activate a virtual environment (recommended):
```bash
# Using venv (Python 3)
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Project Structure

```
CanORT/
├── src/
│   ├── core/
│   │   ├── layer.py    # Layer class for individual canopy layers
│   │   └── canopy.py   # Canopy class for managing multiple layers
│   └── io/
│       └── make_medium.py  # Functions for creating layers and canopies
├── examples/
│   └── make_layer.py   # Example script demonstrating usage
├── requirements.txt
├── setup.py
└── README.md
```

## Usage

```python
from src.core import Layer, Canopy
from src.io import make_layer, make_canopy

# Create a layer
layer = make_layer(
    height=1.0,
    thickness=0.5,
    leaf_area_index=0.8,
    leaf_thickness=0.001,
    temperature=293.15
)

# Create a canopy with arrays of parameters
import numpy as np

thicknesses = np.array([0.5, 1.0, 1.0])
leaf_thicknesses = np.array([0.001, 0.002, 0.001])
temperatures = np.array([293.15, 294.15, 295.15])
leaf_area_indices = np.array([0.2, 0.5, 0.8])

canopy = make_canopy(
    thicknesses=thicknesses,
    leaf_thicknesses=leaf_thicknesses,
    temperatures=temperatures,
    leaf_area_indices=leaf_area_indices
)
print(canopy)

```

## Features

- Layer-based canopy representation
- Leaf area index calculations
- Temperature and leaf thickness tracking
- Array-based canopy creation
- Uniform canopy generation
- Extensible architecture for radiative transfer modeling

## Requirements

- Python >= 3.7
- NumPy >= 1.21.0
- SciPy >= 1.7.0
- Matplotlib >= 3.4.0

## License

MIT License 