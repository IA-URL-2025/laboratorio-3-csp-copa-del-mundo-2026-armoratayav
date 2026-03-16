import pytest
from src.world_cup_csp import WorldCupCSP

# Datos simplificados para pruebas de restricciones
TEST_TEAMS = {
    "Arg": {"conf": "CONMEBOL", "pot": 1},
    "Bra": {"conf": "CONMEBOL", "pot": 2},
    "Fra": {"conf": "UEFA", "pot": 1},
    "Esp": {"conf": "UEFA", "pot": 2},
    "Ger": {"conf": "UEFA", "pot": 3},
    "Mex": {"conf": "CONCACAF", "pot": 1},
    "Jpn": {"conf": "AFC", "pot": 1},
}
TEST_GROUPS = ["A", "B", "C"]

def test_confederation_constraint_non_uefa():
    """Prueba que no se puedan asignar dos equipos de la misma confederación (no UEFA) al mismo grupo."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    assignment = {"Arg": "A"}
    # Intentar asignar a Brasil (CONMEBOL) al grupo A donde ya está Argentina
    assert csp.is_valid_assignment("A", "Bra", assignment) == False
    # Asignarlo a B debería ser válido (asumiendo diferentes bombos, lo cual es cierto aquí)
    assert csp.is_valid_assignment("B", "Bra", assignment) == True

def test_uefa_limit():
    """Prueba que UEFA pueda tener hasta 2 equipos en un grupo, pero no 3."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    # Grupo A ya tiene 2 equipos de UEFA
    assignment = {"Fra": "A", "Esp": "A"}
    # Intentar asignar un tercer equipo de UEFA (Ger) al grupo A debe fallar
    assert csp.is_valid_assignment("A", "Ger", assignment) == False

def test_pot_constraint():
    """Prueba que no se puedan asignar dos equipos del mismo bombo al mismo grupo."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    assignment = {"Arg": "A"} # Bombo 1
    # Intentar asignar otro equipo del bombo 1 (Fra) al grupo A
    assert csp.is_valid_assignment("A", "Fra", assignment) == False

def test_group_size():
    """Prueba que un grupo no pueda exceder los 4 equipos."""
    csp = WorldCupCSP(TEST_TEAMS, ["A"])
    # Asignación inicial con 4 equipos ficticios de diferentes bombos y confederaciones
    # Necesitamos equipos extra para simular un grupo lleno.
    csp.teams = {
        "T1": {"conf": "AFC", "pot": 1},
        "T2": {"conf": "CAF", "pot": 2},
        "T3": {"conf": "CONCACAF", "pot": 3},
        "T4": {"conf": "OFC", "pot": 4},
        "T5": {"conf": "CONMEBOL", "pot": 5} # Extra team
    }
    assignment = {"T1": "A", "T2": "A", "T3": "A", "T4": "A"}
    # Intentar asignar un quinto equipo al grupo A
    assert csp.is_valid_assignment("A", "T5", assignment) == False

def test_valid_assignment():
    """Prueba una asignación completamente válida."""
    csp = WorldCupCSP(TEST_TEAMS, TEST_GROUPS)
    assignment = {"Arg": "A"}
    # Asignar España (UEFA, Bombo 2) al Grupo A (con Arg - CONMEBOL, Bombo 1)
    assert csp.is_valid_assignment("A", "Esp", assignment) == True
