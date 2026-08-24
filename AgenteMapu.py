from AgenteIA.AgenteBuscador import AgenteBuscador


class AgenteMapu(AgenteBuscador):

    def __init__(self):

        AgenteBuscador.__init__(self)

        # Estado inicial:
        # [pacificos izquierda, verdugos izquierda, bote izquierda]
        self.set_estado_inicial([3, 3, 1])

        # Estado meta:
        # todos los personajes en la derecha
        self.set_estado_meta([0, 0, 0])

        # busqueda en anchura
        self.set_tecnica("anchura")

        self.add_funcion(self.pasa_aa)

    def pasa_aa(self, e):

        p, v, bote = e

        hijos = []

        # Posibles combinaciones:
        movimientos = [
            [1, 0],
            [0, 1],
            [2, 0],
            [0, 2],
            [1, 1]
        ]

        for mp, mv in movimientos:

            # BOTE EN LA IZQUIERDA
            if bote == 1:

                # Verificar que existan suficientes personajes
                if mp <= p and mv <= v:

                    nuevo_p = p - mp
                    nuevo_v = v - mv
                    nuevo_bote = 0

                    nuevo_estado = [
                        nuevo_p,
                        nuevo_v,
                        nuevo_bote
                    ]

                    if self.es_valido(nuevo_estado):
                        hijos.append(nuevo_estado)

            # BOTE EN LA DERECHA
            else:

                # Personajes que están en la derecha
                p_derecha = 3 - p
                v_derecha = 3 - v

                # hay suficientes personajes?
                if mp <= p_derecha and mv <= v_derecha:

                    nuevo_p = p + mp
                    nuevo_v = v + mv
                    nuevo_bote = 1

                    nuevo_estado = [
                        nuevo_p,
                        nuevo_v,
                        nuevo_bote
                    ]

                    if self.es_valido(nuevo_estado):
                        hijos.append(nuevo_estado)

        return hijos

    def es_valido(self, estado):

        p_izq, v_izq, bote = estado

        # Cantidades que quedan en la derecha
        p_der = 3 - p_izq
        v_der = 3 - v_izq

        # Verificar rangos
        if p_izq < 0 or p_izq > 3:
            return False

        if v_izq < 0 or v_izq > 3:
            return False

        # Verificar orilla izquierda
        if p_izq > 0 and v_izq > p_izq:
            return False

        # Verificar orilla derecha
        if p_der > 0 and v_der > p_der:
            return False

        return True

    def programa(self):

        AgenteBuscador.programa(self)

        camino = self.get_acciones()

        #  de camino de estados a instrucciones
        self.set_acciones(
            self.obtener_instrucciones(camino)
        )

    def obtener_instrucciones(self, camino):

        instrucciones = []

        for i in range(len(camino) - 1):

            actual = camino[i]
            siguiente = camino[i + 1]

            p_actual = actual[0]
            v_actual = actual[1]
            bote_actual = actual[2]

            p_siguiente = siguiente[0]
            v_siguiente = siguiente[1]

            diferencia_p = p_siguiente - p_actual
            diferencia_v = v_siguiente - v_actual

            # Bote va hacia la derecha
            if bote_actual == 1:

                cantidad_p = -diferencia_p
                cantidad_v = -diferencia_v

                direccion = "a la derecha"
                verbo = "Lleva"

            # Bote vuelve hacia la izquierda
            else:

                cantidad_p = diferencia_p
                cantidad_v = diferencia_v

                direccion = "a la izquierda"
                verbo = "Trae"

            partes = []

            if cantidad_p > 0:

                if cantidad_p == 1:
                    partes.append("1 pacífico")
                else:
                    partes.append(
                        str(cantidad_p) + " pacíficos"
                    )

            if cantidad_v > 0:

                if cantidad_v == 1:
                    partes.append("1 verdugo")
                else:
                    partes.append(
                        str(cantidad_v) + " verdugos"
                    )

            instruccion = (
                verbo + " " +
                " y ".join(partes) +
                " " +
                direccion + "."
            )

            instrucciones.append(instruccion)

        return instrucciones