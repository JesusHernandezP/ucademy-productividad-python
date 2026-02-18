from input_utils import pedir_entero_rango
from task_service import menu_tareas


def menu_principal(state: dict):
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión de tareas")
        print("2. Gestión de hábitos")
        print("3. Búsqueda y filtros")
        print("4. Estadísticas")
        print("5. Registro de sesión")
        print("6. Salir")

        opcion = pedir_entero_rango("Selecciona una opción (1-6): ", 1, 6)

        if opcion == 1:
            menu_tareas(state)

        elif opcion == 2:
            print("Gestión de hábitos (pendiente implementar)")
        elif opcion == 3:
            print("Búsqueda y filtros (pendiente implementar)")
        elif opcion == 4:
            print("Estadísticas (pendiente implementar)")
        elif opcion == 5:
            print("Registro de sesión (pendiente implementar)")
        elif opcion == 6:
            print("\n⚠️ Los datos no se guardan. Al salir se perderá todo.")
            break
