from datetime import datetime
from input_utils import (
    pedir_texto_obligatorio,
    pedir_entero_rango,
    pedir_fecha_opcional,
    pedir_etiquetas,
    pedir_entero_opcional,
)


def menu_tareas(state: dict):
    while True:
        print("\n===== GESTIÓN DE TAREAS =====")
        print("1. Crear tarea")
        print("2. Listar tareas")
        print("3. Ver detalle")
        print("4. Cambiar estado")
        print("5. Editar tarea")
        print("6. Eliminar tarea")
        print("7. Plan del día")
        print("8. Volver")

        opcion = pedir_entero_rango("Selecciona una opción (1-8): ", 1, 8)

        if opcion == 1:
            crear_tarea(state)
        elif opcion == 2:
            listar_tareas(state)
        elif opcion == 3:
            ver_detalle_tarea(state)
        elif opcion == 4:
            cambiar_estado_tarea(state)
        elif opcion == 5:
            editar_tarea(state)
        elif opcion == 6:
            eliminar_tarea(state)
        elif opcion == 7:
            plan_del_dia(state)
        elif opcion == 8:
            break

def eliminar_tarea(state: dict):
    if not state["tareas"]:
        print("\nNo hay tareas creadas.")
        return

    tarea_id = pedir_entero_rango(
        "Introduce el ID de la tarea a eliminar: ",
        1,
        state["next_task_id"] - 1
    )

    tarea = next(
        (t for t in state["tareas"] if t["id"] == tarea_id),
        None
    )

    if not tarea:
        print("❌ Tarea no encontrada.")
        return

    print("\n=== CONFIRMACIÓN DE ELIMINACIÓN ===")
    print(f"ID: {tarea['id']}")
    print(f"Título: {tarea['titulo']}")
    print(f"Estado: {tarea['estado']}")

    confirmacion = input(
        "Escribe exactamente ELIMINAR para confirmar: "
    ).strip()

    if confirmacion != "ELIMINAR":
        print("❌ Eliminación cancelada.")
        return

    state["tareas"] = [
        t for t in state["tareas"] if t["id"] != tarea_id
    ]

    state["log_sesion"].append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": "ELIMINAR_TAREA",
            "detalle": f"Tarea {tarea_id} eliminada",
        }
    )

    print("✅ Tarea eliminada correctamente.")


def editar_tarea(state: dict):
    if not state["tareas"]:
        print("\nNo hay tareas creadas.")
        return

    tarea_id = pedir_entero_rango(
        "Introduce el ID de la tarea a editar: ",
        1,
        state["next_task_id"] - 1
    )

    tarea = next(
        (t for t in state["tareas"] if t["id"] == tarea_id),
        None
    )

    if not tarea:
        print("❌ Tarea no encontrada.")
        return

    cambios = []

    print("\n=== EDITAR TAREA (ENTER mantiene valor actual) ===")

    # TÍTULO
    nuevo_titulo = input(
        f"Título actual [{tarea['titulo']}]: "
    ).strip()

    if nuevo_titulo:
        if len(nuevo_titulo) > 60:
            print("❌ Máximo 60 caracteres. Cambio ignorado.")
        else:
            cambios.append(f"titulo: {tarea['titulo']} → {nuevo_titulo}")
            tarea["titulo"] = nuevo_titulo

    # DESCRIPCIÓN
    nueva_desc = input(
        f"Descripción actual [{tarea['descripcion'] or '-'}]: "
    ).strip()

    if nueva_desc:
        cambios.append("descripcion actualizada")
        tarea["descripcion"] = nueva_desc

    # PRIORIDAD
    nueva_prioridad = input(
        f"Prioridad actual [{tarea['prioridad']}]: "
    ).strip()

    if nueva_prioridad:
        try:
            nueva_prioridad = int(nueva_prioridad)
            if 1 <= nueva_prioridad != tarea["prioridad"]:
                cambios.append(
                    f"prioridad: {tarea['prioridad']} → {nueva_prioridad}"
                )
                tarea["prioridad"] = nueva_prioridad
            else:
                print("❌ Prioridad inválida. Cambio ignorado.")
        except ValueError:
            print("❌ Prioridad inválida. Cambio ignorado.")

    # FECHA VENCIMIENTO
    nueva_fecha = input(
        f"Fecha vencimiento actual [{tarea['fecha_vencimiento'] or '-'}]: "
    ).strip()

    if nueva_fecha:
        try:
            datetime.strptime(nueva_fecha, "%Y-%m-%d")
            cambios.append(
                f"fecha_vencimiento actualizada"
            )
            tarea["fecha_vencimiento"] = nueva_fecha
        except ValueError:
            print("❌ Fecha inválida. Cambio ignorado.")

    # ETIQUETAS
    nuevas_etiquetas = input(
        f"Etiquetas actuales [{', '.join(tarea['etiquetas']) or '-'}]: "
    ).strip()

    if nuevas_etiquetas:
        etiquetas = [
            e.strip().lower()
            for e in nuevas_etiquetas.split(",")
            if e.strip()
        ]
        cambios.append("etiquetas actualizadas")
        tarea["etiquetas"] = etiquetas

    # TIEMPO ESTIMADO
    nuevo_tiempo = input(
        f"Tiempo estimado actual [{tarea['tiempo_estimado_min'] or '-'}]: "
    ).strip()

    if nuevo_tiempo:
        try:
            nuevo_tiempo = int(nuevo_tiempo)
            if nuevo_tiempo >= 0:
                cambios.append(
                    f"tiempo_estimado actualizado"
                )
                tarea["tiempo_estimado_min"] = nuevo_tiempo
            else:
                print("❌ Debe ser >= 0. Cambio ignorado.")
        except ValueError:
            print("❌ Valor inválido. Cambio ignorado.")

    if cambios:
        state["log_sesion"].append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "accion": "EDITAR_TAREA",
                "detalle": f"Tarea {tarea_id}: " + "; ".join(cambios),
            }
        )
        print("✅ Tarea actualizada correctamente.")
    else:
        print("ℹ No se realizaron cambios.")



def crear_tarea(state: dict):
    print("\n=== CREAR TAREA ===")

    titulo = pedir_texto_obligatorio("Título: ", max_len=60)
    descripcion = input("Descripción (opcional): ").strip()

    prioridad = pedir_entero_rango(
        "Prioridad (1=baja, 2=media, 3=alta): ", 1, 3
    )

    fecha_vencimiento = pedir_fecha_opcional(
        "Fecha de vencimiento (YYYY-MM-DD) o ENTER: "
    )

    etiquetas = pedir_etiquetas(
        "Etiquetas (ej: casa, urgente, python): "
    )

    tiempo_estimado = pedir_entero_opcional(
        "Tiempo estimado en minutos (ENTER si no aplica): "
    )

    tarea = {
        "id": state["next_task_id"],
        "titulo": titulo,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": "pendiente",
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
        "fecha_vencimiento": fecha_vencimiento,
        "etiquetas": etiquetas,
        "tiempo_estimado_min": tiempo_estimado,
        "tiempo_real_min": None,
    }

    state["tareas"].append(tarea)
    state["next_task_id"] += 1

    state["log_sesion"].append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": "CREAR_TAREA",
            "detalle": f"Tarea {tarea['id']} - {titulo}",
        }
    )

    print("✅ Tarea creada correctamente.")


def listar_tareas(state: dict):
    if not state["tareas"]:
        print("\nNo hay tareas creadas.")
        return

    print("\n=== ORDENAR POR ===")
    print("1. Prioridad (alta → baja)")
    print("2. Fecha de vencimiento")
    print("3. Estado")
    print("4. Título (A → Z)")

    opcion = pedir_entero_rango("Selecciona orden (1-4): ", 1, 4)

    tareas = state["tareas"][:]

    if opcion == 1:
        tareas.sort(key=lambda x: x["prioridad"], reverse=True)

    elif opcion == 2:
        tareas.sort(
            key=lambda x: (
                x["fecha_vencimiento"] is None,
                x["fecha_vencimiento"] or ""
            )
        )

    elif opcion == 3:
        orden_estado = {
            "pendiente": 1,
            "en_progreso": 2,
            "hecha": 3,
            "cancelada": 4,
        }
        tareas.sort(key=lambda x: orden_estado.get(x["estado"], 99))

    elif opcion == 4:
        tareas.sort(key=lambda x: x["titulo"].lower())

    print("\n=== LISTADO DE TAREAS ===")
    print("ID | P | ESTADO       | VENCE       | TÍTULO")
    print("-" * 65)

    for t in tareas:
        vence = t["fecha_vencimiento"] or "-"
        print(
            f"{t['id']:2} | "
            f"{t['prioridad']} | "
            f"{t['estado']:12} | "
            f"{vence:10} | "
            f"{t['titulo']}"
        )


def ver_detalle_tarea(state: dict):
    if not state["tareas"]:
        print("\nNo hay tareas creadas.")
        return

    tarea_id = pedir_entero_rango(
        "Introduce el ID de la tarea: ",
        1,
        state["next_task_id"] - 1
    )

    tarea = next(
        (t for t in state["tareas"] if t["id"] == tarea_id),
        None
    )

    if not tarea:
        print("❌ Tarea no encontrada.")
        return

    print("\n===== DETALLE DE TAREA =====")
    print(f"ID: {tarea['id']}")
    print(f"Título: {tarea['titulo']}")
    print(f"Descripción: {tarea['descripcion'] or '-'}")
    print(f"Prioridad: {tarea['prioridad']}")
    print(f"Estado: {tarea['estado']}")
    print(f"Fecha creación: {tarea['fecha_creacion']}")
    print(f"Fecha vencimiento: {tarea['fecha_vencimiento'] or '-'}")
    print(
        "Etiquetas: "
        + (", ".join(tarea["etiquetas"]) if tarea["etiquetas"] else "-")
    )
    print(f"Tiempo estimado: {tarea['tiempo_estimado_min'] or '-'}")
    print(f"Tiempo real: {tarea['tiempo_real_min'] or '-'}")


def cambiar_estado_tarea(state: dict):
    if not state["tareas"]:
        print("\nNo hay tareas creadas.")
        return

    tarea_id = pedir_entero_rango(
        "Introduce el ID de la tarea: ",
        1,
        state["next_task_id"] - 1
    )

    tarea = next(
        (t for t in state["tareas"] if t["id"] == tarea_id),
        None
    )

    if not tarea:
        print("❌ Tarea no encontrada.")
        return

    print(f"\nEstado actual: {tarea['estado']}")
    print("1. pendiente")
    print("2. en_progreso")
    print("3. hecha")
    print("4. cancelada")
    print("5. Cancelar")

    opcion = pedir_entero_rango("Selecciona nuevo estado (1-5): ", 1, 5)

    if opcion == 5:
        return

    estados = {
        1: "pendiente",
        2: "en_progreso",
        3: "hecha",
        4: "cancelada",
    }

    nuevo_estado = estados[opcion]

    if tarea["estado"] == "hecha" and nuevo_estado == "en_progreso":
        confirmacion = input(
            "La tarea está hecha. Escribe SI para confirmar cambio: "
        ).strip()

        if confirmacion != "SI":
            print("Cambio cancelado.")
            return

    if nuevo_estado == "hecha":
        tiempo_real = pedir_entero_opcional(
            "¿Tiempo real en minutos? (ENTER para 0): "
        )
        tarea["tiempo_real_min"] = tiempo_real or 0

    estado_anterior = tarea["estado"]
    tarea["estado"] = nuevo_estado

    state["log_sesion"].append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": "CAMBIAR_ESTADO",
            "detalle": f"Tarea {tarea_id}: {estado_anterior} → {nuevo_estado}",
        }
    )

    print("✅ Estado actualizado correctamente.")

    def plan_del_dia(state: dict):
        if not state["tareas"]:
            print("\nNo hay tareas creadas.")
        return

    hoy = datetime.now().strftime("%Y-%m-%d")

    vencidas = []
    hoy_lista = []
    pendientes = []
    en_progreso = []
    otras = []

    for t in state["tareas"]:
        fecha = t["fecha_vencimiento"]

        if fecha and fecha < hoy:
            vencidas.append(t)
        elif fecha == hoy:
            hoy_lista.append(t)
        elif t["estado"] == "pendiente":
            pendientes.append(t)
        elif t["estado"] == "en_progreso":
            en_progreso.append(t)
        else:
            otras.append(t)

    # Ordenar por prioridad descendente
    pendientes.sort(key=lambda x: x["prioridad"], reverse=True)
    en_progreso.sort(key=lambda x: x["prioridad"], reverse=True)

    print("\n===== PLAN DEL DÍA =====")

    def imprimir_bloque(nombre, lista):
        if lista:
            print(f"\n--- {nombre} ---")
            for t in lista:
                vence = t["fecha_vencimiento"] or "-"
                print(
                    f"ID: {t['id']} | P:{t['prioridad']} | "
                    f"Estado: {t['estado']} | Vence: {vence} | {t['titulo']}"
                )

    imprimir_bloque("TAREAS VENCIDAS", vencidas)
    imprimir_bloque("TAREAS PARA HOY", hoy_lista)
    imprimir_bloque("PENDIENTES (por prioridad)", pendientes)
    imprimir_bloque("EN PROGRESO", en_progreso)
    imprimir_bloque("OTRAS (hechas/canceladas)", otras)

    print("\n(Enter para volver)")
    input()

