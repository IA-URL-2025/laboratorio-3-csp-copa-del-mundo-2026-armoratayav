import pytest
from src.world_cup_csp import WorldCupCSP

# Datos simplificados para pruebas de heurísticas
TEST_TEAMS = {
    "T1": {"conf": "UEFA", "pot": 1},
    "T2": {"conf": "CONMEBOL", "pot": 2},
    "T3": {"conf": "CONCACAF", "pot": 3},
    "T4": {"conf": "AFC", "pot": 4},
}
TEST_GROUPS = ["A", "B", "C"]

def test_mrv_selection():
    """Prueba que la heurística MRV seleccione la variable con el dominio más pequeño."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    # Todos están sin asignar, pero alteramos los dominios artificialmente para forzar MRV
    domains = {
        "T1": ["A", "B", "C"],
        "T2": ["B"], # T2 tiene solo 1 opción
        "T3": ["A", "C"],
        "T4": ["C", "B"]
    }
    assignment = {}

    # La variable seleccionada debería ser T2 ya que tiene el dominio más pequeño (1 valor)
    var = csp.select_unassigned_variable(assignment, domains)
    assert var == "T2"

def test_mrv_with_assigned_variables():
    """Prueba que MRV ignore las variables ya asignadas."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    domains = {
        "T1": ["A", "B"],
        "T2": ["B"], # T2 tiene dominio pequeño, pero ya está asignado
        "T3": ["C"], # T3 tiene dominio pequeño y NO está asignado
        "T4": ["A", "B", "C"]
    }
    assignment = {"T2": "B"} # T2 ya asignado

    var = csp.select_unassigned_variable(assignment, domains)
    # Debería seleccionar T3, no T2, porque T2 ya está asignado.
    assert var == "T3"

def test_forward_checking():
    """Prueba que forward checking elimine valores inconsistentes de los dominios."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    # Dominios iniciales completos
    domains = {t: list(TEST_GROUPS) for t in TEST_TEAMS.keys()}

    # Supongamos que asignamos T1 al grupo A
    assignment = {"T1": "A"}

    # Supongamos que T2 y T1 comparten el mismo bombo (pot) para forzar una restricción
    csp.teams["T2"]["pot"] = 1 # Ahora T1 y T2 son del Bombo 1

    success, new_domains = csp.forward_check(assignment, domains)

    assert success == True
    # El grupo A ya no debería estar en el dominio de T2 porque chocarían en el bombo 1
    assert "A" not in new_domains["T2"]
    # Los otros grupos sí deberían estar
    assert "B" in new_domains["T2"]
    assert "C" in new_domains["T2"]

def test_forward_checking_failure():
    """Prueba que forward checking falle y retorne False si un dominio queda vacío."""
    csp = WorldCupCSP(TEST_TEAMS, ["A"]) # Solo un grupo disponible
    domains = {t: ["A"] for t in TEST_TEAMS.keys()}

    # Modificamos los datos para forzar un fallo. T1 y T2 del mismo bombo
    csp.teams["T2"]["pot"] = 1

    assignment = {"T1": "A"}

    # Forward check intentará ver si T2 puede ir a A, verá que no (mismo bombo),
    # y como solo hay grupo A, su dominio quedará vacío.
    success, new_domains = csp.forward_check(assignment, domains)

    # Debería fallar
    assert success == False
    assert len(new_domains["T2"]) == 0
