from abc import ABC, abstractmethod

from partituras.modelo.errores import (
    ContieneNumero,
    ContieneCaracterInvalido,
    SinNotas,
    EspacioMultiple,
    EspacioBordes
)


class ReglaTransformacion(ABC):

    NOTAS = ["mi", "fa", "sol", "la", "si", "do", "re"]

    def __init__(self, token: int):
        self.token = token

    @abstractmethod
    def transformar(self, partitura: str) -> str:
        pass

    @abstractmethod
    def revertir(self, partitura: str) -> str:
        pass

    @abstractmethod
    def partitura_valida(self, partitura: str) -> bool:
        pass

    def encontrar_numeros_partitura(self, partitura: str) -> list:
        return [
            (i, c)
            for i, c in enumerate(partitura)
            if c.isdigit()
        ]

    def encontrar_caracteres_invalidos(self, partitura: str) -> list:
        return [
            (i, c)
            for i, c in enumerate(partitura)
            if ord(c) > 127
        ]


class ReglaTransposicion(ReglaTransformacion):

    def partitura_valida(self, partitura: str) -> bool:

        errores = []

        numeros = self.encontrar_numeros_partitura(partitura)
        if numeros:
            mensaje = ", ".join(
                [f"{c} en posicion {i}" for i, c in numeros]
            )
            errores.append(
                ContieneNumero(
                    f"ContieneNumero: {mensaje}"
                )
            )

        invalidos_ascii = self.encontrar_caracteres_invalidos(partitura)
        if invalidos_ascii:
            mensaje = ", ".join(
                [f"{c} en posicion {i}" for i, c in invalidos_ascii]
            )
            errores.append(
                ContieneCaracterInvalido(
                    f"ContieneCaracterInvalido: {mensaje}"
                )
            )

        tokens = partitura.lower().split()

        permitidos = self.NOTAS + ["|", "-"]

        invalidos = [
            token for token in tokens
            if token not in permitidos
        ]

        if invalidos:
            errores.append(
                ContieneCaracterInvalido(
                    f"ContieneCaracterInvalido: {invalidos}"
                )
            )

        notas = [
            token for token in tokens
            if token in self.NOTAS
        ]

        if not notas:
            errores.append(
                SinNotas("SinNotas")
            )

        if errores:
            raise ExceptionGroup(
                " ".join(str(e) for e in errores),
                errores
            )

        return True

    def transformar(self, partitura: str) -> str:

        self.partitura_valida(partitura)

        tokens = partitura.lower().split()

        resultado = [
            self._transponer(token, self.token)
            if token in self.NOTAS
            else token
            for token in tokens
        ]

        return " ".join(resultado)

    def revertir(self, partitura: str) -> str:

        self.partitura_valida(partitura)

        tokens = partitura.lower().split()

        resultado = [
            self._transponer(token, -self.token)
            if token in self.NOTAS
            else token
            for token in tokens
        ]

        return " ".join(resultado)

    def _transponer(self, nota, desplazamiento):

        indice = self.NOTAS.index(nota)

        nuevo_indice = (indice + desplazamiento) % len(self.NOTAS)

        return self.NOTAS[nuevo_indice]


class ReglaFrecuencia(ReglaTransformacion):

    FRECUENCIAS = {
        "do": 261,
        "re": 293,
        "mi": 329,
        "fa": 349,
        "sol": 392,
        "la": 440,
        "si": 493
    }

    def partitura_valida(self, partitura: str) -> bool:

        errores = []

        numeros = self.encontrar_numeros_partitura(partitura)
        if numeros:
            mensaje = ", ".join(
                [f"{c} en posicion {i}" for i, c in numeros]
            )
            errores.append(
                ContieneNumero(
                    f"ContieneNumero: {mensaje}"
                )
            )

        invalidos_ascii = self.encontrar_caracteres_invalidos(partitura)
        if invalidos_ascii:
            mensaje = ", ".join(
                [f"{c} en posicion {i}" for i, c in invalidos_ascii]
            )
            errores.append(
                ContieneCaracterInvalido(
                    f"ContieneCaracterInvalido: {mensaje}"
                )
            )

        if partitura != partitura.strip():
            errores.append(
                EspacioBordes("EspacioBordes")
            )

        if "  " in partitura:
            errores.append(
                EspacioMultiple("EspacioMultiple")
            )

        tokens = partitura.lower().split()

        invalidos = [
            token for token in tokens
            if token not in self.NOTAS
        ]

        if invalidos:
            errores.append(
                ContieneCaracterInvalido(
                    f"ContieneCaracterInvalido: {invalidos}"
                )
            )

        if errores:
            raise ExceptionGroup(
                " ".join(str(e) for e in errores),
                errores
            )

        return True

    def transformar(self, partitura: str) -> str:

        self.partitura_valida(partitura)

        tokens = partitura.lower().split()

        resultado = [
            str(self.FRECUENCIAS[token] * self.token)
            for token in tokens
        ]

        return " ".join(resultado)

    def revertir(self, partitura: str) -> str:

        valores = [
            int(x)
            for x in partitura.split()
        ]

        resultado = []

        for valor in valores:

            frecuencia = valor // self.token

            nota = next(
                nota
                for nota, freq in self.FRECUENCIAS.items()
                if freq == frecuencia
            )

            resultado.append(nota)

        return " ".join(resultado)


class Compositor:

    def __init__(self, interprete: ReglaTransformacion):
        self.interprete = interprete

    def transformar(self, partitura: str) -> str:
        return self.interprete.transformar(partitura)

    def revertir(self, partitura: str) -> str:
        return self.interprete.revertir(partitura)