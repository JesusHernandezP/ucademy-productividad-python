from menus import menu_principal


def main():
    state = {
        "tareas": [],
        "habitos": [],
        "log_sesion": [],
        "next_task_id": 1,
        "next_habit_id": 1,
    }

    menu_principal(state)


if __name__ == "__main__":
    main()
