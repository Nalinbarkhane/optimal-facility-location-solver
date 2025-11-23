# Mathematical Model Formulation

This document details the mathematical model for the **Capacitated Facility Location Problem (CFLP)** used in this project.

## Overview

The CFLP is a Mixed-Integer Programming (MIP) problem. The goal is to select a subset of potential facility sites to open and to determine the flow of goods from these open facilities to a set of customers. The model minimizes the sum of fixed opening costs and variable transportation costs, subject to demand and capacity constraints.

---

## 1. Sets and Indices

* $I$: The set of potential facility locations (e.g., $i \in \{\text{DC1}, \text{DC2}, ...\}$).
* $J$: The set of customer regions (e.g., $j \in \{\text{Cust1}, \text{Cust2}, ...\}$).

---

## 2. Parameters

* $f_i$: The fixed cost to open and operate a facility at site $i$, for $i \in I$.
* $C_i$: The maximum capacity (in units) of a facility at site $i$, for $i \in I$.
* $d_j$: The total demand (in units) from customer $j$, for $j \in J$.
* $t_{ij}$: The variable cost to transport one unit of product from facility $i$ to customer $j$, for $i \in I$ and $j \in J$. (In this project, this is calculated based on Euclidean distance).

---

## 3. Decision Variables

* **$y_i$ (Binary):**
    A binary variable that equals 1 if the facility at site $i$ is opened, and 0 otherwise.
    $$
    y_i \in \{0, 1\} \quad \forall i \in I
    $$

* **$x_{ij}$ (Continuous):**
    A continuous variable representing the quantity of product shipped from facility $i$ to customer $j$.
    $$
    x_{ij} \ge 0 \quad \forall i \in I, j \in J
    $$

---

## 4. Objective Function

The objective is to **minimize** the total cost, which is the sum of all fixed costs for opened facilities and all variable transportation costs for shipped goods.

$$
\text{Minimize} \quad Z = \sum_{i \in I} (f_i \cdot y_i) + \sum_{i \in I} \sum_{j \in J} (t_{ij} \cdot x_{ij})
$$

---

## 5. Constraints

The solution must adhere to the following rules:

1.  **Demand Satisfaction:**
    All demand from each customer must be met exactly.
    $$
    \sum_{i \in I} x_{ij} = d_j \quad \forall j \in J
    $$

2.  **Capacity Constraint:**
    The total amount of product shipped *from* a facility cannot exceed its capacity. This constraint also links the $x$ and $y$ variables, ensuring that shipping can only occur *from* an *open* facility.
    $$
    \sum_{j \in J} x_{ij} \le C_i \cdot y_i \quad \forall i \in I
    $$
    *(Note: If $y_i = 0$, the right side becomes 0, forcing all $x_{ij}$ for that facility to be 0.)*