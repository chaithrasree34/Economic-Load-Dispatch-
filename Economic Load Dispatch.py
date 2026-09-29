# Economic-Load-Dispatch-
import numpy as np

# ============================================================
# ECONOMIC LOAD DISPATCH USING LAMBDA ITERATION
# ============================================================

print("=" * 65)
print("             ECONOMIC LOAD DISPATCH")
print("              Lambda Iteration Method")
print("=" * 65)

# ------------------------------------------------------------
# NUMBER OF GENERATING UNITS
# ------------------------------------------------------------

n = int(input("\nEnter number of generating units: "))

# Arrays for fuel-cost coefficients
a = np.zeros(n)
b = np.zeros(n)
c = np.zeros(n)

Pmin = np.zeros(n)
Pmax = np.zeros(n)

# ------------------------------------------------------------
# INPUT GENERATOR DATA
# ------------------------------------------------------------

print("\nEnter generator data:")
print("Fuel cost: F(P) = a + bP + cP^2")

for i in range(n):
    print(f"\nGenerator {i + 1}")

    a[i] = float(input("Enter a: "))
    b[i] = float(input("Enter b: "))
    c[i] = float(input("Enter c: "))

    Pmin[i] = float(input("Enter minimum power Pmin (MW): "))
    Pmax[i] = float(input("Enter maximum power Pmax (MW): "))

# ------------------------------------------------------------
# LOAD DEMAND
# ------------------------------------------------------------

PD = float(input("\nEnter total load demand (MW): "))

# Check whether demand is possible
if PD < np.sum(Pmin) or PD > np.sum(Pmax):
    print("\nERROR: Load demand is outside generation limits.")
    print(f"Minimum generation = {np.sum(Pmin):.2f} MW")
    print(f"Maximum generation = {np.sum(Pmax):.2f} MW")
    exit()

# ------------------------------------------------------------
# LAMBDA ITERATION
# ------------------------------------------------------------

# Initial lambda limits
lambda_low = 0.0
lambda_high = 100.0

tolerance = 0.00001
max_iterations = 1000

for iteration in range(max_iterations):

    lam = (lambda_low + lambda_high) / 2

    P = np.zeros(n)

    # Calculate generation for each unit
    for i in range(n):

        # dF/dP = b + 2cP = lambda
        P[i] = (lam - b[i]) / (2 * c[i])

        # Apply generator limits
        if P[i] < Pmin[i]:
            P[i] = Pmin[i]

        elif P[i] > Pmax[i]:
            P[i] = Pmax[i]

    total_generation = np.sum(P)

    # Check convergence
    error = total_generation - PD

    if abs(error) < tolerance:
        break

    # Adjust lambda
    if total_generation > PD:
        lambda_high = lam
    else:
        lambda_low = lam

# ------------------------------------------------------------
# FUEL COST CALCULATION
# ------------------------------------------------------------

fuel_cost = np.zeros(n)

for i in range(n):
    fuel_cost[i] = (
        a[i]
        + b[i] * P[i]
        + c[i] * P[i] ** 2
    )

total_cost = np.sum(fuel_cost)

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("                 ELD RESULTS")
print("=" * 65)

print(f"\nNumber of iterations : {iteration + 1}")
print(f"Lambda               : {lam:.6f}")
print(f"Load demand          : {PD:.4f} MW")
print(f"Total generation     : {total_generation:.4f} MW")
print(f"Power mismatch       : {error:.8f} MW")

print("\nGenerator Results")
print("-" * 65)

print(
    f"{'Unit':<8}"
    f"{'Pmin(MW)':<12}"
    f"{'Pmax(MW)':<12}"
    f"{'Output(MW)':<15}"
    f"{'Fuel Cost':<15}"
)

print("-" * 65)

for i in range(n):
    print(
        f"{i + 1:<8}"
        f"{Pmin[i]:<12.2f}"
        f"{Pmax[i]:<12.2f}"
        f"{P[i]:<15.4f}"
        f"{fuel_cost[i]:<15.4f}"
    )

print("-" * 65)

print(f"\nTotal Generation = {np.sum(P):.4f} MW")
print(f"Total Fuel Cost  = {total_cost:.4f}")
print(f"Lambda           = {lam:.6f}")

print("\n" + "=" * 65)
print("             ELD CALCULATION COMPLETED")
print("=" * 65)
