import copy

class WorldCupCSP:
    def __init__(self, teams, groups, debug=False):
        """
        Inicializa el problema CSP para el sorteo del Mundial.
        :param teams: Diccionario con los equipos, sus confederaciones y bombos.
        :param groups: Lista con los nombres de los grupos (A-L).
        :param debug: Booleano para activar trazas de depuración.
        """
        self.teams = teams
        self.groups = groups
        self.debug = debug

        # Las variables son los equipos.
        self.variables = list(teams.keys())

        # El dominio de cada variable inicialmente son todos los grupos.
        self.domains = {team: list(groups) for team in self.variables}

    def get_team_confederation(self, team):
        return self.teams[team]["conf"]

    def get_team_pot(self, team):
        return self.teams[team]["pot"]

    def is_valid_assignment(self, group, team, assignment):
        """
        Verifica si asignar un equipo a un grupo viola
        las restricciones de confederación, bombo o tamaño del grupo.
        """
        team_conf = self.get_team_confederation(team)
        team_pot = self.get_team_pot(team)

        teams_in_group = [assigned_team for assigned_team, assigned_group in assignment.items()
                          if assigned_group == group]

        # Restricción 1: máximo 4 equipos por grupo
        if len(teams_in_group) >= 4:
            return False

        # Restricción 2: no puede haber dos equipos del mismo bombo en el mismo grupo
        for assigned_team in teams_in_group:
            if self.get_team_pot(assigned_team) == team_pot:
                return False

        # Restricción 3: confederaciones
        same_conf_count = 0
        for assigned_team in teams_in_group:
            if self.get_team_confederation(assigned_team) == team_conf:
                same_conf_count += 1

        if team_conf == "UEFA":
            if same_conf_count >= 2:
                return False
        else:
            if same_conf_count >= 1:
                return False

        return True

    def forward_check(self, assignment, domains):
        """
        Propagación de restricciones.
        Elimina valores inconsistentes en dominios futuros.
        Retorna (True, new_domains) si la propagación es exitosa,
        o (False, new_domains) si algún dominio queda vacío.
        """
        new_domains = copy.deepcopy(domains)

        for var in self.variables:
            if var in assignment:
                new_domains[var] = [assignment[var]]
                continue

            valid_values = []
            for group in new_domains[var]:
                if self.is_valid_assignment(group, var, assignment):
                    valid_values.append(group)

            new_domains[var] = valid_values

            if len(new_domains[var]) == 0:
                return False, new_domains

        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):
        """
        Heurística MRV (Minimum Remaining Values).
        Selecciona la variable no asignada con el dominio más pequeño.
        """
        unassigned_vars = [v for v in self.variables if v not in assignment]

        if not unassigned_vars:
            return None

        return min(unassigned_vars, key=lambda var: len(domains[var]))

    def backtrack(self, assignment, domains=None):
        """
        Backtracking search para resolver el CSP.
        """
        if domains is None:
            domains = copy.deepcopy(self.domains)

        # Si todas las variables están asignadas, terminamos.
        if len(assignment) == len(self.variables):
            return assignment

        # 1. Seleccionar variable con MRV
        var = self.select_unassigned_variable(assignment, domains)
        if var is None:
            return assignment

        # 2. Probar cada valor del dominio
        for group in domains[var]:
            # 3. Verificar consistencia local
            if self.is_valid_assignment(group, var, assignment):
                new_assignment = assignment.copy()
                new_assignment[var] = group

                # 4. Aplicar forward checking
                success, new_domains = self.forward_check(new_assignment, domains)

                # 5. Llamada recursiva si no hubo contradicción
                if success:
                    result = self.backtrack(new_assignment, new_domains)
                    if result is not None:
                        return result

        # 6. Si nada funcionó, backtrack
        return None