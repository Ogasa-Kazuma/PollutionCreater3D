# 3D Pollution Simulation

## Overview

This project is a Python-based tool for simulating and visualizing pollution in a 3D space. It allows users to create custom 3D fields, add multiple spherical pollution sources with varying sizes and concentrations, and then visualize the resulting pollution distribution. The simulation data can also be saved to a file for further analysis.

## File Descriptions

- **`PointClass.py`**: Defines the `Point` class, which represents a point in 3D space (x, y, z) and includes methods for calculating distances.
- **`Pollution_Creater.py`**: Contains the `PollutionCreater` class, used to generate spherical pollution data around a central point.
- **`Pollution.py`**: The core of the project. It defines the `Pollution` class, which manages the 3D pollution data as a NumPy array. It provides methods for adding pollution sources, visualizing the data with `matplotlib`, and saving the data to CSV or pickle files.
- **`Data_Saver.py`**: A generic class for saving data structures to a pickle file using `pandas`.
- **`main.py`**: Currently empty. The primary example of how to use the library is in `test/Pollution_Creater.py`.
- **`test/Pollution_Creater.py`**: An example script demonstrating how to create a pollution field, add spherical pollution sources, and then view and save the results.

## How to Run the Example

The main usage example is located in `test/Pollution_Creater.py`. To run it, you need Python installed with the following libraries:
- `numpy`
- `pandas`
- `matplotlib`

You can install them using pip:
```bash
pip install numpy pandas matplotlib
```

After installing the dependencies, you can run the example from the root directory of the project:

```bash
python test/Pollution_Creater.py
```

This will run the simulation, print some pollution values to the console, display a 3D plot of the pollution, and save the output to `PollutionLog/unko.csv`. Note that you may need to create the `PollutionLog` directory first.
