def menu_estadisticas(state):
    print("\n===== ESTADÍSTICAS =====")

    total = len(state["tareas"])
    hechas = len([t for t in state["tareas"] if t["estado"] == "hecha"])

    if total > 0:
        porcentaje = round((hechas / total) * 100, 1)
    else:
        porcentaje = 0

    print(f"Total de tareas: {total}")
    print(f"Tareas completadas: {hechas}")
    print(f"Porcentaje de cumplimiento: {porcentaje}%")

    por_prioridad = {1: 0, 2: 0, 3: 0}
    for t in state["tareas"]:
        por_prioridad[t["prioridad"]] += 1

    print("\nTareas por prioridad:")
    for p, cantidad in por_prioridad.items():
        print(f"- Prioridad {p}: {cantidad}")

    tiempo_estimado = sum(
        t["tiempo_estimado_min"] or 0 for t in state["tareas"]
    )
    tiempo_real = sum(
        t["tiempo_real_min"] or 0 for t in state["tareas"]
    )

    print(f"\nTiempo estimado total: {tiempo_estimado} min")
    print(f"Tiempo real total: {tiempo_real} min")

    print("\n(ENTER para volver)")
    input()
