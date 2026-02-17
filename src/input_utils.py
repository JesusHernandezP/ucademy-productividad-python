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
