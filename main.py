from src.solver import run_solver, print_solution
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solver CSP para el Sorteo del Mundial 2026')
    parser.add_argument('--debug', action='store_true', help='Activa el modo depuración (trazas de ejecución)')
    args = parser.parse_args()

    # Run the solver with debug mode if requested
    print(f"Modo debug: {'Activado' if args.debug else 'Desactivado'}")
    solution = run_solver(debug=args.debug, preassign_pots_1_2=True)

    if solution:
        print_solution(solution)
    else:
        print("\nNo se pudo encontrar una asignación válida para todos los equipos.")
