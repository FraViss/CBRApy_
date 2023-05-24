from pyomo.environ import *

#Create a simple model
m = ConcreteModel()
m.x = Var()
m.y = Var()
m.obj = Objective(expr=m.x**2 + m.y**2)
m.c = Constraint(expr=m.y >= -2*m.x + 5)

#Invoke the multistart solver
SolverFactory('multistart').solve(m)  