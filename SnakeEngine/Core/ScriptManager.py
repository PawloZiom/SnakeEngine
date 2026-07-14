from .GameScript import GameScript


class ScriptManager:
    def __init__(self):

        self._started_scripts = set()

    def _get_active_scripts(self, entities):

        active_scripts = []
        for entity in entities:
            if not entity.IsActive:
                continue
            for comp in entity.Components.values():
                if isinstance(comp, GameScript):
                    active_scripts.append(comp)
        return active_scripts

    def OnStart(self, entities):

        current_active = self._get_active_scripts(entities)
        for script in current_active:
            if script not in self._started_scripts:
                script.OnStart()
                self._started_scripts.add(script)

    def OnUpdate(self, entities, delta_time: float):

        self.OnStart(entities)

        current_active = self._get_active_scripts(entities)
        for script in current_active:
            if script in self._started_scripts:
                script.OnUpdate(delta_time)

    def OnFixedUpdate(self, entities, fixed_delta_time: float):

        current_active = self._get_active_scripts(entities)
        for script in current_active:
            if script in self._started_scripts:
                script.OnFixedUpdate(fixed_delta_time)

    def ClearOrphanedScripts(self, entities):
        """Czyści wewnętrzny kesz managera ze skryptów, których encje zostały usunięte.

        Zapobiega wyciekom pamięci (Memory Leaks). Wywołuj np. przy zmianie sceny.
        """
        all_current_scripts = set()
        for entity in entities:
            for comp in entity.Components.values():
                if isinstance(comp, GameScript):
                    all_current_scripts.add(comp)

        self._started_scripts.intersection_update(all_current_scripts)
