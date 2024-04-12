# Variable polyline buffer

## Description

`variable_polyline_buffer` is a Python library for calculating a buffer around a polyline, defining the contours of a line with variable thickness. This function supports various applications in geographical information systems, computer graphics, and spatial analysis where dynamic line thickness is required.

## Installation

To install this package, use pip:

```bash
pip install variable_polyline_buffer
```

## Usage

Here is a simple example of how to use Variable-Polyline-Buffer:

```python
from variable_polyline_buffer import generate_polyline_buffer
import matplotlib.pyplot as plt

# Example data: coordinates of polyline points and distance for each segment
points = [(0, 0), (2, 0.5), (3, -0.5), (4, 1)]
distances = [1, 0.5, 0.2]  # Thickness of the individual segments

# Generate contours
left_contour, right_contour = generate_polyline_buffer(points, distances)

# Plot the contours
plt.plot([p[0] for p in points], [p[1] for p in points], "C0")
plt.plot([p[0] for p in left_contour], [p[1] for p in left_contour], "k--")
plt.plot([p[0] for p in right_contour], [p[1] for p in right_contour], "k--")
plt.axis("equal")
```

![Output image](https://github.com/stephtr/variable-polyline-buffer/raw/main/imgs/1.svg)

Replace points and dists with your polyline data and corresponding thicknesses.

Via supplying tuples as dists, one can also generate different thicknesses on the curve's two sides:

```python
points = [(0, 0), (2, 0.5), (3, -0.5), (4, 1)]
distances = [(0.1, 1), (0.1, 0.5), 0.2]
```

![Output image](https://github.com/stephtr/variable-polyline-buffer/raw/main/imgs/2.svg)

By supplying `False` as distance, one can taper between segments with different widths:

```python
points = [(0, 0), (1, 0), (2, 0), (3, 0)]
distances = [(0.5, 0), (False, 0), (0.2, 0)]
```

![Output image](https://github.com/stephtr/variable-polyline-buffer/raw/main/imgs/3.svg)

## Requirements

Variable-Polyline-Buffer requires the following Python libraries:

- NumPy

## License

This project is licensed under the MIT License.
