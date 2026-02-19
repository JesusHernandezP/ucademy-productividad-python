from datetime import datetime
from utils import pedir_entero_rango, pedir_no_vacio, pedir_opcional

def menu_habitos(state: dict):
    while True:
        print("\n===== GESTIÓN DE HÁBITOS =====")
        print("1. Crear hábito")
        print("2. Registrar cumplimiento")
        print("3. Listar hábitos")
        print("4. Ver historial")
        print("5. Editar hábito")
        print("6. Eliminar hábito")
        print("7. Volver")

        op = pedir_entero_rango("Selecciona una opción (1-7): ", 1, 7)

        if op == 1:
            crear_habito(state)
        elif op == 2:
            registrar_cumplimiento(state)
        elif op == 3:
            listar_habitos(state)
        elif op == 4:
            ver_historial(state)
        elif op == 5:
            editar_habito(state)
        elif op == 6:
            eliminar_habito(state)
        else:
            return


def crear_habito(state: dict):
    print("\n=== CREAR HÁBITO ===")

    nombre = pedir_no_vacio("Nombre del hábito: ")
    periodicidad = pedir_entero_rango(
        "Periodicidad (1=diario, 2=semanal, 3=mensual): ", 1, 3
    )
    objetivo = pedir_entero_rango("Objetivo (ej: 1 vez por día): ", 1, 50)
    etiquetas = input("Etiquetas (ej: salud, estudio): ").strip()

    etiquetas_list = []
    if etiquetas:
        etiquetas_list = [x.strip() for x in etiquetas.split(",")]

    habito = {
        "id": state["next_habit_id"],
        "nombre": nombre,
        "periodicidad": periodicidad,
        "objetivo": objetivo,
        "cumplimientos": [],
        "etiquetas": etiquetas_list,
        "creado": datetime.now().strftime("%Y-%m-%d")
    }

    state["habitos"].append(habito)
    state["next_habit_id"] += 1

    state["log_sesion"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": "CREAR_HABITO",
        "detalle": f"Hábito {habito['id']} - {habito['nombre']}"
    })

    print("✅ Hábito creado correctamente.")


def registrar_cumplimiento(state: dict):
    if not state["habitos"]:
        print("\nNo hay hábitos creados.")
        return

    listar_habitos(state)
    hid = pedir_entero_rango("Ingresa ID del hábito: ", 1, 9999)

    hab = next((h for h in state["habitos"] if h["id"] == hid), None)
    if not hab:
        print("❌ ID no encontrado.")
        return

    hoy = datetime.now().strftime("%Y-%m-%d")

    hab["cumplimientos"].append(hoy)

    state["log_sesion"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": "REGISTRO_HABITO",
        "detalle": f"Hábito {hab['id']} - {hab['nombre']}"
    })

    print("✅ Cumplimiento registrado.")


def listar_habitos(state: dict):
    print("\n=== LISTADO DE HÁBITOS ===")

    if not state["habitos"]:
        print("No hay hábitos.")
        return

    for h in state["habitos"]:
        n = len(h["cumplimientos"])
        print(
            f"ID: {h['id']} | Nombre: {h['nombre']} | Objetivo: {h['objetivo']} | "
            f"Cumplimientos: {n} | Etiquetas: {', '.join(h['etiquetas']) if h['etiquetas'] else '-'}"
        )


def ver_historial(state: dict):
    hid = pedir_entero_rango("ID del hábito: ", 1, 9999)

    hab = next((h for h in state["habitos"] if h["id"] == hid), None)
    if not hab:
        print("❌ No existe el hábito.")
        return

    print(f"\n=== HISTORIAL DE {hab['nombre']} ===")

    if not hab["cumplimientos"]:
        print("Sin registros.")
        return

    for fecha in hab["cumplimientos"]:
        print(f"- {fecha}")


def editar_habito(state: dict):
    hid = pedir_entero_rango("ID del hábito a editar: ", 1, 9999)

    hab = next((h for h in state["habitos"] if h["id"] == hid), None)
    if not hab:
        print("❌ No existe el hábito.")
        return

    print("\n=== EDITAR HÁBITO (ENTER mantiene) ===")

    nuevo_nombre = pedir_opcional(f"Nombre [{hab['nombre']}]: ")
    nueva_period = pedir_opcional(f"Periodicidad [{hab['periodicidad']}]: ")
    nuevo_obj = pedir_opcional(f"Objetivo [{hab['objetivo']}]: ")
    nuevas_et = pedir_opcional("Etiquetas (coma) o ENTER: ")

    if nuevo_nombre:
        hab["nombre"] = nuevo_nombre

    if nueva_period:
        if nueva_period.isdigit() and 1 <= int(nueva_period) <= 3:
            hab["periodicidad"] = int(nueva_period)

    if nuevo_obj:
        if nuevo_obj.isdigit():
            hab["objetivo"] = int(nuevo_obj)

    if nuevas_et:
        hab["etiquetas"] = [x.strip() for x in nuevas_et.split(",")]

    print("✅ Hábito actualizado.")


def eliminar_habito(state: dict):
    hid = pedir_entero_rango("ID del hábito a eliminar: ", 1, 9999)
    hab = next((h for h in state["habitos"] if h["id"] == hid), None)

    if not hab:
        print("❌ No existe.")
        return

    print("\n=== CONFIRMACIÓN ===")
    print(f"ID: {hab['id']} | Nombre: {hab['nombre']}")
    conf = input("Escribe ELIMINAR para confirmar: ")

    if conf != "ELIMINAR":
        print("❌ Cancelado.")
        return

    state["habitos"].remove(hab)
    print("✅ Eliminado correctamente.")
