# menus.py

from task_service import menu_tareas
from habit_service import menu_habitos
from filter_service import menu_filtros
from stats_service import menu_estadisticas
from log_service import menu_log

def menu_principal(state: dict):
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión de tareas")
        print("2. Gestión de hábitos")
        print("3. Búsqueda y filtros")
        print("4. Estadísticas")
        print("5. Registro de sesión")
        print("6. Salir")

        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            menu_tareas(state)
        elif opcion == "2":
            menu_habitos(state)
        elif opcion == "3":
            menu_filtros(state)
        elif opcion == "4":
            menu_estadisticas(state)
        elif opcion == "5":
            menu_log(state)
        elif opcion == "6":
            print("Saliendo...")
            return
        else:
            print("❌ Opción no válida.")
