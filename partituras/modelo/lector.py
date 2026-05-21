import json

from partituras.modelo.errores import (ArchivoNoEncontrado, ArchivoCorrupto)


class LectorPartituras:

    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo

    def cargar(self) -> list[str]:

        try:

            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:

                datos = json.load(archivo)

                return datos["partituras"]

        except FileNotFoundError as e:
            raise ArchivoNoEncontrado(
                "ArchivoNoEncontrado"
            ) from e

        except json.JSONDecodeError as e:
            raise ArchivoCorrupto(
                "ArchivoCorrupto"
            ) from e

    def procesar_con(self, compositor):

        partituras = self.cargar()

        return [
            self._procesar_partitura(compositor, partitura)
            for partitura in partituras
        ]

    def _procesar_partitura(self, compositor, partitura):

        try:

            transformada = compositor.transformar(partitura)

            revertida = compositor.revertir(transformada)

            return {
                "original": partitura,
                "transformada": transformada,
                "revertida": revertida,
                "exito": True,
                "errores": []
            }

        except ExceptionGroup as eg:

            return {
                "original": partitura,
                "transformada": None,
                "revertida": None,
                "exito": False,
                "errores": [
                    str(error)
                    for error in eg.exceptions
                ]
            }

        except Exception as e:

            return {
                "original": partitura,
                "transformada": None,
                "revertida": None,
                "exito": False,
                "errores": [str(e)]
            }