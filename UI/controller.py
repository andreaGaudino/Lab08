import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view._txtOut.clean()
        self._view.update_page()
        nerc_name = self._view._ddNerc.value
        nerc_id = None
        for i in self._idMap:
            if i == nerc_name:
                nerc_id = self._idMap[i].id
        maxY = int(self._view._txtYears.value)
        maxH = int(self._view._txtHours.value)
        max_persone, soluzione, tot_ore = self._model.worstCase(nerc_id, maxY, maxH)
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected: {max_persone}"))
        self._view._txtOut.controls.append(ft.Text(f"Tot hours of outages: {tot_ore}"))
        for i in soluzione:
            self._view._txtOut.controls.append(ft.Text(f"{i.__str__()}"))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
