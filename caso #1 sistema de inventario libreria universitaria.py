
import simpy
import random

# Parámetros
TIEMPO_SIMULACION = 30
TIEMPO_ENTRE_CLIENTES = 1.5
TIEMPO_ENTRE_PEDIDOS = 3
PUNTO_REORDEN = 20
CANTIDAD_PEDIDO = 50
INVENTARIO_INICIAL = 40

inventario = INVENTARIO_INICIAL
pedido_pendiente = False


def llegada_clientes(env):
    global inventario, pedido_pendiente

    cliente = 0

    while True:
        tiempo = random.expovariate(1 / TIEMPO_ENTRE_CLIENTES)
        yield env.timeout(tiempo)

        cliente += 1

        if inventario > 0:
            inventario -= 1
            print(
                f"Día {env.now:.2f}: Cliente {cliente} compra 1 libro. Inventario = {inventario}"
            )

            if inventario <= PUNTO_REORDEN and not pedido_pendiente:
                pedido_pendiente = True
                env.process(realizar_pedido(env))

        else:
            print(
                f"Día {env.now:.2f}: Cliente {cliente} no pudo comprar. Inventario agotado."
            )


def realizar_pedido(env):
    global inventario, pedido_pendiente

    print(f"Día {env.now:.2f}: Pedido realizado al proveedor.")

    yield env.timeout(TIEMPO_ENTRE_PEDIDOS)

    inventario += CANTIDAD_PEDIDO
    pedido_pendiente = False

    print(
        f"Día {env.now:.2f}: Pedido recibido. Inventario actualizado = {inventario}"
    )


env = simpy.Environment()

env.process(llegada_clientes(env))

env.run(until=TIEMPO_SIMULACION)