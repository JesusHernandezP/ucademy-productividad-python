from utils import pedir_entero_rango, pedir_no_vacio

def menu_filtros(state: dict):
    while True:
        print("\n===== BÚSQUEDA Y FILTROS =====")
        print("1. Buscar por texto")
        print("2. Filtrar por prioridad")
        print("3. Filtrar por estado")
        print("4. Filtrar por etiqueta")
        print("5. Filtro combinado")
        print("6. Volver")

        op = pedir_entero_rango("Opción (1-6): ", 1, 6)

        if op == 1:
            buscar_texto(state)
        elif op == 2:
            filtrar_prioridad(state)
        elif op == 3:
            filtrar_estado(state)
        elif op == 4:
            filtrar_etiqueta(state)
        elif op == 5:
            filtro_combinado(state)
        else:
            return


def buscar_texto(state):
    texto = pedir_no_vacio("Buscar: ").lower()
    resultados = [
        t for t in state["tareas"]
        if texto in t["titulo"].lower() or texto in (t["descripcion"] or "").lower()
    ]
    mostrar(resultados)


def filtrar_prioridad(state):
    p = pedir_entero_rango("Prioridad (1-3): ", 1, 3)
    resultados = [t for t in state["tareas"] if t["prioridad"] == p]
    mostrar(resultados)


def filtrar_estado(state):
    est = pedir_no_vacio("Estado (pendiente, en_progreso, hecha, cancelada): ")
    resultados = [t for t in state["tareas"] if t["estado"] == est]
    mostrar(resultados)


def filtrar_etiqueta(state):
    et = pedir_no_vacio("Etiqueta: ")
    resultados = [t for t in state["tareas"] if et in t["etiquetas"]]
    mostrar(resultados)


def filtro_combinado(state):
    print("\n== Filtro combinado ==")
    p = pedir_opcional("Prioridad (1-3) o ENTER: ")
    e = pedir_opcional("Estado o ENTER: ")
    et = pedir_opcional("Etiqueta o ENTER: ")

    resultados = state["tareas"]

    if p and p.isdigit():
        resultados = [t for t in resultados if t["prioridad"] == int(p)]

    if e:
        resultados = [t for t in resultados if t["estado"] == e]

    if et:
        resultados = [t for t in resultados if et in t["etiquetas"]]

    mostrar(resultados)


def mostrar(lista):
    if not lista:
        print("\nSin resultados.")
        return

    print("\n=== RESULTADOS ===")
    for t in lista:
        vence = t["fecha_vencimiento"] or "-"
        print(
            f"ID: {t['id']} | Título: {t['titulo']} | Prioridad: {t['prioridad']} | "
            f"Estado: {t['estado']} | Vence: {vence}"
        )
