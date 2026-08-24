from AgenteMapu import AgenteMapu


agente = AgenteMapu()

agente.programa()

acciones = agente.get_acciones()

print("SOLUCIÓN:")
print()

for i, accion in enumerate(acciones):
    print(i + 1, accion)