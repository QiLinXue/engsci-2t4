import numpy as np
self_weight = 8e-3
P = 1000
reaction_force = (P)/2 + 0.123*30
bridge_span = 980


bridge_loads = [
    (0, 15, reaction_force/15),
    (15, 265, -self_weight),
    (265, 295, -P/60 - self_weight),
    (295, 655, -self_weight),
    (655, 685, -P/60 - self_weight),
    (685, 935, - self_weight),
    (935, 950, reaction_force/15),
]



import sympy as sym
x = sym.symbols('x')
f = sym.Piecewise(
    (reaction_force/30      ,x  < 30  ),
    (-self_weight           ,x  < 280 ),
    ( -P/60 - self_weight   ,x < 310),
    ( -self_weight          ,x < 670),
    ( -P/60 - self_weight   ,x < 700),
    ( - self_weight         ,x < 950),
    ( reaction_force/30     ,x < 980),
    (0, True)
)

precision = 980
x_points = np.linspace(0,bridge_span,precision)

shear_generator = sym.integrate(f)
moment_generator = sym.integrate(shear_generator)

shear_force = np.zeros(precision)
moment = np.zeros(precision)

for i in range(len(x_points)):
    shear_force[i] = shear_generator.subs(x,i)

for i in range(len(x_points)):
    moment[i] = moment_generator.subs(x,i)

import matplotlib.pyplot as plt
plt.figure()
plt.plot(x_points, shear_force)
plt.title("Moment Diagram")
plt.ylabel("Moment (N mm)")
plt.xlabel("Location (mm)")
plt.show()
