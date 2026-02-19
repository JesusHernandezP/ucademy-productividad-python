def menu_log(state):
    logs = state["log_sesion"]

    if not logs:
        print("\nSin registros.")
        return

    pagina = 0
    por_pag = 10

    while True:
        print("\n===== REGISTRO DE SESIÓN =====")
        inicio = pagina * por_pag
        fin = inicio + por_pag

        for log in logs[inicio:fin]:
            print(f"{log['timestamp']} | {log['accion']} | {log['detalle']}")

        print("\nn = siguiente | p = anterior | 0 = volver")
        op = input(">> ").lower()

        if op == "n" and fin < len(logs):
            pagina += 1
        elif op == "p" and pagina > 0:
            pagina -= 1
        elif op == "0":
            return
