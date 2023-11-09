from pyomo.environ import *

model = ConcreteModel()

# Define el conjunto de índices PERIOD
model.PERIOD = Set(initialize=[1, 2, 3, 4])  # Reemplaza los elementos con los adecuados

# Define el nombre de la variable que deseas crear
nombre = "StoA"  # Puedes cambiar esto al nombre que desees

# Define el valor de x
x = 5.0  # Reemplaza 5.0 por el valor que desees

# Utiliza setattr para crear la variable dinámicamente en el modelo
setattr(model, nombre, Var(model.PERIOD, within=NonNegativeReals, initialize=x))

# Luego, puedes acceder a la variable deseada de la siguiente manera:
period = 1  # Reemplaza 1 por el período que desees
variable_deseada = getattr(model, nombre)

# Puedes acceder al valor de la variable deseada para un período específico
value_of_variable = value(variable_deseada[period])

print(f"Valor de {nombre} para el período {period}: {value_of_variable}")
