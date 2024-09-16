import math
from random import random, randint
from graphics import *

DURATA_TURNO             = 1000 # ms
NUM_PERSONAGGI           = 20
DIM_PERSONAGGIO          = 20.0 # px
PASSO_PERSONAGGIO        = 15.0 # px
PUNTI_VITA_PERSONAGGIO   = 3 # PV
PUNTI_VITA_ARCIERE       = 5 # PV
PUNTI_VITA_BOMBAROLO     = 6 # PV
VISTA_ARCIERE            = 160.0 # px
DANNO_ARCIERE            = 1 # PV
RAGGIO_BOMBAROLO         = 120.0 # px
DANNO_BOMBAROLO          = 3 # PV
COLORE_SFONDO            = 'slategray'
COLORE_TESTO             = 'white'
COLORE_PERSONAGGIO       = 'cadetblue3'
COLORE_ARCIERE           = 'darkgreen'
COLORE_TRAIETTORIA       = 'white'
COLORE_BOMBAROLO         = 'brown1'
COLORE_BOMBAROLO_RAGGIO  = 'coral'

class Personaggio:
    def __init__(self, x, y, punti_vita=PUNTI_VITA_PERSONAGGIO):
        self.punti_vita = punti_vita
        self.x = x
        self.y = y
        self.angolo_mov = 2.0 * math.pi * random()

    def is_vivo(self):
        return (self.punti_vita > 0)

    def disegna(self):
        self._disegna_forma()
        draw_text(self.x, self.y, COLORE_TESTO, '{}'.format(self.punti_vita))

    def _disegna_forma(self):
        draw_circle(self.x, self.y, COLORE_PERSONAGGIO, DIM_PERSONAGGIO)

    def muovi(self, passo=PASSO_PERSONAGGIO):
        if self.is_vivo():
            tocca_bordo = (self.x <= DIM_PERSONAGGIO or self.y <= DIM_PERSONAGGIO or self.x >= SCREEN_WIDTH - DIM_PERSONAGGIO - 1 or self.y >= SCREEN_HEIGHT - DIM_PERSONAGGIO - 1)
            if tocca_bordo or randint(1, 12) == 1:
                # - se la posizione è sul bordo dell schermo oppure
                # - il lancio di un dado a 12 facce dà come esito 1 (~8.3% dei casi)
                # Ruota la direzione di movimento di un angolo casuale tra -45° e +45°
                self.angolo_mov = (self.angolo_mov + math.pi * (random() - 0.5)) % (2.0 * math.pi)
            
            # Calcola la direzione di movimento (normalizzata, cioè di lunghezza 1.0)
            muovi_dirx = math.cos(self.angolo_mov)
            muovi_diry = math.sin(self.angolo_mov)

            # Aggiorna la posizione, controllando di non uscire dallo schermo
            self.x = min(max(self.x + passo * muovi_dirx, DIM_PERSONAGGIO), SCREEN_WIDTH - DIM_PERSONAGGIO - 1)
            self.y = min(max(self.y + passo * muovi_diry, DIM_PERSONAGGIO), SCREEN_HEIGHT - DIM_PERSONAGGIO - 1)
            
    def turno(self, _personaggi):
        self.muovi()
    
    def ricevi_danno(self, danno):
        if self.punti_vita > danno:
            self.punti_vita -= danno
        else:
            self.punti_vita = 0
    
    def get_distanza_da(self, altro):
        distx = self.x - altro.x
        disty = self.y - altro.y
        return math.sqrt(distx * distx + disty * disty)
    
    def get_piu_vicino(self, personaggi):
        piu_vicino = None
        dist_piu_vicino = math.inf
        for altro in personaggi:
            if altro != self:
                d = self.get_distanza_da(altro)
                if d < dist_piu_vicino:
                    piu_vicino = altro
                    dist_piu_vicino = d
        return piu_vicino

    def get_piu_vicini_di(self, personaggi, max_dist):
        piu_vicini = []
        for altro in personaggi:
            if altro != self:
                if self.get_distanza_da(altro) <= max_dist:
                    piu_vicini.append(altro)
        return piu_vicini

class Arciere(Personaggio):
    def __init__(self, x, y, punti_vita=PUNTI_VITA_ARCIERE):
        super().__init__(x, y, punti_vita)

    def _disegna_forma(self):
        draw_rect(self.x, self.y, COLORE_ARCIERE, 1.6 * DIM_PERSONAGGIO, 1.6 * DIM_PERSONAGGIO)

    def turno(self, personaggi):
        if self.is_vivo():
            if not self.attacca(personaggi):
                self.muovi()

    def attacca(self, personaggi):
        altro = self.get_piu_vicino(personaggi)
        if altro and self.get_distanza_da(altro) <= VISTA_ARCIERE:
            draw_line(self.x, self.y, COLORE_TRAIETTORIA, altro.x, altro.y)
            altro.ricevi_danno(DANNO_ARCIERE)
            return True
        return False

class Bombarolo(Personaggio):
    def __init__(self, x, y, punti_vita=PUNTI_VITA_BOMBAROLO):
        super().__init__(x, y, punti_vita)
    
    def _disegna_forma(self):
        draw_circle(self.x, self.y, COLORE_BOMBAROLO, DIM_PERSONAGGIO, 0)

    def turno(self, personaggi):
        if self.is_vivo():
            if not self.attacca(personaggi):
                self.muovi()

    def attacca(self, personaggi):
        altri = self.get_piu_vicini_di(personaggi, RAGGIO_BOMBAROLO)
        if len(altri) > 0:
            for altro in altri:
                altro.ricevi_danno(DANNO_BOMBAROLO)
            draw_circle(self.x, self.y, COLORE_BOMBAROLO_RAGGIO, RAGGIO_BOMBAROLO, 1)
            return True
        return False

# Funzioni di gestione del gioco
def crea_personaggi(n):
    personaggi = []
    for _i in range(n):
        # Genera una coppia di coordinate casuali all'interno dello schermo
        x = DIM_PERSONAGGIO + random() * (SCREEN_WIDTH - DIM_PERSONAGGIO - 1)
        y = DIM_PERSONAGGIO + random() * (SCREEN_HEIGHT - DIM_PERSONAGGIO - 1)
        
        match randint(1, 3): # Tira un D3
            case 1: # Crea un personaggio semplice
                p = Personaggio(x, y)
            case 2: # Crea un arciere
                p = Arciere(x, y)
            case 3: # Crea un bombarolo
                p = Bombarolo(x, y)
        personaggi.append(p)
    return personaggi

# Funzione principale
def main():
    personaggi = crea_personaggi(NUM_PERSONAGGI)
    turno = 1
    while len(personaggi) > 1 and not quit_requested():
        # Pulisci lo schermo
        screen.fill(COLORE_SFONDO)
        screen.blit(sysfont.render('Turno: {}'.format(turno), True, 'white', 'black'), (2, 2))

        # Esegui il turno di tutti i personaggi ancora in gioco
        for p in personaggi:
            p.turno(personaggi)
        
        # Disegna tutti i personaggi
        for p in personaggi:
            p.disegna()

        # Aggiorna lo schermo e attendi per *DURATA_TURNO* millisecondi
        pygame.display.flip()
        pygame.time.wait(DURATA_TURNO)

        # Aggiorna l'elenco dei personaggi ancora in vita
        personaggi_vivi = []
        for p in personaggi:
            if p.is_vivo():
                personaggi_vivi.append(p)
        personaggi = personaggi_vivi

        turno += 1

    if len(personaggi) == 1:
        while not quit_requested():
            pygame.time.wait(100)
            
    pygame.quit()
            
main()
