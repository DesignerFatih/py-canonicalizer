# py-canonicalizer: A Universal Tool for Polyline Canonicalization
	- This Python package is designed to solve a common problem in computational geometry and CAD workflows: the arbitrary start-point and direction of polylines. It provides a robust, universal algorithm to standardize 3D point lists, making them predictable and ready for further processing by algorithms like the Ramer-Douglas-Peucker (RDP) algorithm.
	- This ensures that your algorithmic results are consistent every time, regardless of the original data's orientation.
- ## Features
	- **Application-Agnostic:** Works with any Python environment, with no dependencies on specific CAD or GIS software.
	- **Rule-Based Standardization:** Uses a clear, hierarchical set of rules (based on centroid proximity and coordinate values) to define a canonical starting point and direction.
	- **Data Cleaning:** Automatically handles duplicate points in closed polylines to prevent calculation errors.
- ## Installation
	- You can install the package directly from PyPI using pip:
	- ```bash
	  pip install py-canonicalizer
	  ```
- ## Usage
	- The core function `canonicalize_points` takes a NumPy array and returns a new, ordered array.
	- ```
	  import numpy as np
	  from py_canonicalizer import canonicalize_points
	  
	  # Example: a simple closed polyline with an arbitrary start point
	  original_points = np.array([[1, 1, 0], [2, 3, 0], [5, 4, 0], [4, 1, 0], [1, 1, 0]])
	  
	  # Get the canonicalized version
	  canonical_points = canonicalize_points(original_points)
	  
	  print(canonical_points)
	  # Output will always be consistently ordered regardless of the input's original orientation.
	  ```
- ## How It Works
	- The algorithm is based on a set of rules and a hierarchical tie-breaker system to ensure a single, repeatable result for any given point cloud.
	- **Data Cleaning:** The algorithm first removes duplicate points, which often appear at the end of closed polylines.
	- **Canonical Start Point:** It finds the point closest to the geometric center (centroid) of the polyline.
	- **Hierarchical Tie-breaker:** If multiple points are equally close, it uses a predictable rule (max X, then max Y, then max Z) to select the starting point.
	- **Direction:** It then compares the neighbors of the start point using the same tie-breaker rule to determine the polyline's final, standardized direction (e.g., clockwise vs. counter-clockwise).
	- <img width="484" height="471" alt="resim" src="https://github.com/user-attachments/assets/8bc8e955-3f9d-4649-908a-b8aa6ea7e8ee" />
	- Behavior of the canonicalization algorithm in the square edge case. Since all vertices are equidistant from the center, the algorithm applies hierarchical sorting rules (Max X → Max Y) to designate C(1,1) as the starting point. The red curved arrow represents the deterministic orientation decision made by evaluating the coordinate magnitudes of neighboring vertices, while the blue straight arrows indicate the final data sequence in which the geometry is stored in memory.
- ## License
	- This project is licensed under the MIT License.
