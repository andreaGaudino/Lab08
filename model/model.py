import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self._persone_max = -1



    def worstCase(self, nerc, maxY, maxH):
        self.loadEvents(nerc)
        # for evento in self._listEvents:
        self.ricorsione([], maxY, maxH, 0)
        # print(self._persone_max)
        # for i in self._solBest:
        #     print(i._id, end=" ")
        # print()
        tot_ore = 0
        for el in self._solBest:
            tot_ore += ((el._date_event_finished - el._date_event_began).total_seconds()) / 3600
        return self._persone_max, self._solBest, tot_ore


    def ricorsione(self, parziale, maxY, maxH, pos):

        #primo = self._listEvents[pos]
        #condizione terminale
        # if pos == len(self._listEvents):
        #     conteggio = self.calcola_persone(parziale)
        #     if conteggio > self._persone_max:
        #         self._persone_max = conteggio
        #         self._solBest = parziale
        #         for i in self._solBest:
        #             print(i.__str__(), end=" ")
        #         print()
        # else:
            #parziale.append(primo)
            lista = self._listEvents[pos:]
            for elem in lista:
                if self.vincoli(parziale, elem, maxY, maxH):
                    parziale.append(elem)
                    parziale = sorted(parziale, key=lambda evento: evento._date_event_began)
                    self.ricorsione(parziale, maxY, maxH, lista.index(elem))
                    parziale.remove(elem)


            conteggio = self.calcola_persone(parziale)
            if conteggio > self._persone_max:
                self._persone_max = conteggio
                self._solBest = copy.deepcopy(parziale)



    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

    def calcola_persone(self, parziale):
        conto = 0
        for i in range(len(parziale)):
            conto += parziale[i]._customers_affected
        return conto

    def vincoli(self, parziale, elem, maxY, maxH):
        if parziale == []:
            return True

        somma = ((elem._date_event_finished - elem._date_event_began).total_seconds()) / 3600
        # somma=0
        for i in range(len(parziale)):
            somma += ((parziale[i]._date_event_finished - parziale[i]._date_event_began).total_seconds()) / 3600

            if parziale[i]._id == elem._id:
                return False

        if ((elem._date_event_finished.year - parziale[0]._date_event_began.year) <= maxY and somma <= maxH):
            return True
        else:
            return False