# Optimal Facility Location Solver

## Overview

This project is a Python-based solution for the classic Operations Research problem: the **Capacitated Facility Location Problem (CFLP)**. 

Given a set of potential locations for distribution centers (DCs) and a set of customers with known demands, this model determines:
1.  **Which** facilities to build.
2.  **How** to assign customers to those facilities.

The goal is to **minimize the total cost**, which includes the fixed cost of opening each facility and the variable cost of transporting goods to customers. This implementation uses external data files and visualizes the final solution.



---

## Features

* **Data-Driven:** Loads facility and customer data from `.csv` files using `pandas`.
* **Dynamic Costing:** Calculates variable transport costs based on the Euclidean distance between facilities and customers.
* **MIP Solver:** Uses the `PuLP` library to build and solve the Mixed-Integer Program.
* **Visualization:** Generates a plot using `matplotlib` showing the optimal network configuration, including open facilities and shipping routes.

---

## Example Output

After you run the project, a visualization image of the optimal configuration will be saved to `docs/images/solution.png` and a Matplotlib window will be displayed. You can embed the generated image in the README for quick reference as follows:

```markdown
![Optimal Facility Location and Shipping Routes](docs/images/solution.png)
```

You can also view the file directly from the `docs/images/` folder in the repository.

---

## Technology Stack

* **Python 3.x**
* **PuLP:** For modeling and solving the linear programming problem.
* **Pandas:** For data loading and manipulation.
* **Matplotlib:** For visualizing the solution.
* **Scikit-learn:** For calculating the Euclidean distance matrix.

---

## Project Structure

facility-location-project/ 
    ├── index.py # The main Python script 
    ├── facilities.csv # Input data for potential DC sites 
    ├── customers.csv # Input data for customer locations and demand 
    ├── README.md # This file 
    └── docs/ 
        ├── INSTRUCTIONS.md # Setup and execution guide
        └── MODEL_FORMULATION.md # The mathematical model



---

## How to Use

1.  **Install Dependencies:** Ensure you have all the required Python libraries.
    ```bash
    pip install pulp pandas matplotlib scikit-learn
    ```

2.  **Run the Model:**
    ```bash
    python index.py
    ```

3.  **View Results:** The script will print the optimal cost, the facilities to open, and the shipping plan to the console. A new window will also open displaying the solution map.

For more detailed instructions, see `docs/INSTRUCTIONS.md`.
For a full breakdown of the mathematical model, see `docs/MODEL_FORMULATION.md`.