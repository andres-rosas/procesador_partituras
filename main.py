from partituras.modelo.compositor import (
    ReglaTransposicion,
    ReglaFrecuencia,
    Compositor
)

from partituras.modelo.lector import LectorPartituras

from partituras.modelo.errores import (
    ArchivoNoEncontrado,
    ArchivoCorrupto
)


def imprimir_resultados(nombre, resultados):

    print(f"\n===== {nombre} =====\n")

    for resultado in resultados:

        print("Original:", resultado["original"])

        if resultado["exito"]:

            print("Transformada:", resultado["transformada"])
            print("Revertida:", resultado["revertida"])

        else:

            print("Errores:")

            for error in resultado["errores"]:
                print("-", error)

        print()


def main():

    try:

        compositor_transposicion = Compositor(
            ReglaTransposicion(5)
        )

        compositor_frecuencia = Compositor(
            ReglaFrecuencia(5)
        )

        lector = LectorPartituras(
            "partituras_ejemplo.json"
        )

        resultados_transposicion = lector.procesar_con(
            compositor_transposicion
        )

        resultados_frecuencia = lector.procesar_con(
            compositor_frecuencia
        )

        imprimir_resultados(
            "TRANSPOSICION",
            resultados_transposicion
        )

        imprimir_resultados(
            "FRECUENCIA",
            resultados_frecuencia
        )

    except ArchivoNoEncontrado as e:
        print("Error:", e)

    except ArchivoCorrupto as e:
        print("Error:", e)


if __name__ == "__main__":
    main()