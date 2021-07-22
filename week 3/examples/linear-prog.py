c = [400, 500]
A = [[2, 3]]
b = [12]
x0_bounds = (1, 4)
x1_bounds = (1, 10)

from scipy.optimize import linprog

res = linprog(c, A_ub=A, b_ub=b, bounds=[x0_bounds, x1_bounds])
print(res)

if res.success:
    print(f"X1: {round(res.x[0], 10)} hours")
    print(f"X2: {round(res.x[1], 10)} hours")
else:
    print("No solution")
