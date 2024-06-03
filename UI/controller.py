import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None

    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text(f"Selezionare anno dal menù"))
            return None
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo corretamente creato"))
        n, a = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo è costituito di {n} nodi e {a} archi"))
        self._view.update_page()


    def handleDettagli(self, e):
        v0 = self._selectedTeam
        vicini = self._model.getSortedNeighbors(v0)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {v0} con relativo peso dell'arco"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        if self._selectedTeam == None:
            warnings.warn("Squadra non selezionata")
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text(f"Squadra non selezionata"))
        v0 = self._selectedTeam
        self._view._txt_result.controls.clear()
        path = self._model.getPercorso(v0)
        self._view._txt_result.controls.append(ft.Text(f"Lunghezza percorso trovato: {len(path)}"))
        for p in path:
            self._view._txt_result.controls.append(ft.Text(p))
        self._view.update_page()

    def fillDDYear(self):
        years = self._model.getyears()
        yearsDD = map(lambda x: ft.dropdown.Option(x), years)
        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    def handleDDYears(self, e):
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(ft.Text(f"Trovate {len(teams)} nell'anno {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(
                data=t,
                text=t.teamCode,
                on_click=self.readDDTeams
            ))

        self._view.update_page()

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data