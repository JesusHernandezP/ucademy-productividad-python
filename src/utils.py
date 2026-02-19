def pedir_entero_rango(mensaje, minimo, maximo):
    while True:
        valor = input(mensaje).strip()
        if not valor.isdigit():
            print("❌ Debes introducir un número válido")
            continue

        valor = int(valor)
        if valor < minimo or valor > maximo:
            print(f"❌ Debe estar entre {minimo} y {maximo}")
            continue

        return valor


def pedir_no_vacio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            print("❌ No puede estar vacío")
        else:
            return valor


def pedir_opcional(mensaje):
    valor = input(mensaje).strip()
    return valor if valor != "" else None
