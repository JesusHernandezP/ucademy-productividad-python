from datetime import datetime

def pedir_entero_rango(prompt: str, minimo: int, maximo: int) -> int:
    while True:
        valor = input(prompt).strip()
        try:
            numero = int(valor)
            if minimo <= numero <= maximo:
                return numero
            print(f"❌ Debe estar entre {minimo} y {maximo}")
        except ValueError:
            print("❌ Debes introducir un número válido")




def pedir_texto_obligatorio(prompt: str, max_len: int | None = None) -> str:
    while True:
        texto = input(prompt).strip()
        if not texto:
            print("❌ No puede estar vacío.")
            continue
        if max_len and len(texto) > max_len:
            print(f"❌ Máximo {max_len} caracteres.")
            continue
        return texto


def pedir_fecha_opcional(prompt: str) -> str | None:
    while True:
        valor = input(prompt).strip()
        if valor == "":
            return None
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            print("❌ Formato inválido. Usa YYYY-MM-DD.")


def pedir_etiquetas(prompt: str) -> list[str]:
    valor = input(prompt).strip()
    if not valor:
        return []

    etiquetas = [e.strip().lower() for e in valor.split(",")]
    etiquetas = [e for e in etiquetas if e]
    return etiquetas


def pedir_entero_opcional(prompt: str) -> int | None:
    while True:
        valor = input(prompt).strip()
        if valor == "":
            return None
        try:
            numero = int(valor)
            if numero >= 0:
                return numero
            print("❌ Debe ser >= 0")
        except ValueError:
            print("❌ Debes introducir un número válido")
