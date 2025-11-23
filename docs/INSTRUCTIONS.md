# Setup and Execution Guide

This guide provides the steps to set up your environment and run the Optimal Facility Location project.

## 1. Prerequisites

* **Python 3.8** or newer.
* **pip** (Python's package installer).

## 2. Environment Setup

It is highly recommended to use a Python virtual environment to manage dependencies.

1.  **Clone or Download:** Get the project files onto your local machine.
2.  **Open a Terminal:** Navigate into the project's root directory.
    ```bash
    cd path/to/facility-location-project
    ```
3.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```
4.  **Activate the Environment:**
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

## 3. Install Dependencies

With your virtual environment active, install the required libraries:

```bash
pip install pulp pandas matplotlib scikit-learn
```

## 4. Prepare Data Files
The script requires two data files to be present in the main project directory:

1. `facilities.csv`: Contains potential facility locations, fixed costs, and capacities.
2. `customers.csv`: Contains customer locations and their demands.

Ensure these files are correctly formatted and named.

## 5. Run the Project
Execute the main script from your terminal:
```bash
python index.py
```

## 6. Expected Output
When you run the script, you should see two things:

1. Terminal Output: The script will print the status of the solver, the total optimal cost, a list of which facilities to open, and a detailed shipping plan.
2. Visualization Window: A new window from matplotlib will open, displaying a graph of the solution, including customer locations, all potential facility sites, the chosen sites, and the new shipping routes.

3. Saved Plot: The script will also save a copy of the plot to `docs/images/solution.png`. This is useful for sharing and embedding the example image in the README or documentation.

Note: The script calls `plt.show()` which opens a Matplotlib window. If you're running the script in a headless environment (CI, server) you can either remove/comment out `plt.show()` or run inside an X server (like Xvfb) to see the window. The plot is still saved to `docs/images/solution.png` regardless.