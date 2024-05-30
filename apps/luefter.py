# -*- coding: utf-8 -*-

import appdaemon.plugins.hass.hassapi as hass

#
# Lueftersteuerung (in Arbeit)
#
# Args:
#

class LuefterSteuerung(hass.Hass):

    aktiv = None
    automatik = False
    automatik_name = "Nicht konfiguriert"
    luefter_name = "Nicht konfiguriert"
    thermometer_name = "Nicht konfiguriert"
    start_temp = 60.0
    stop_temp = 50.0
    temp_listen_handle = None

    def initialize(self):
        self.log("Lueftersteuerung gestartet.")
        self.automatik_name = self.args["automatik"]
        self.luefter_name = self.args["luefter"]
        self.thermometer_name = self.args["thermometer"]
        self.start_temp = float(self.args["start_temp"])
        self.stop_temp = float(self.args["stop_temp"])
        self.log("Konfiguration: Automatik: %s Lüfter=%s, Thermometer=%s, Start bei %s °C, Stopp bei %s °C", self.automatik_name, self.luefter_name, self.thermometer_name, self.start_temp, self.stop_temp)

        # Wir wollen mitbekommen, ob die Automatik ein- oder ausgeschaltet wird
        self.reagiere_auf_automatik(self.get_state(self.automatik_name))
        self.listen_state(self.automatik_callback, self.automatik_name)

    def automatik_callback(self, entity, attribute, old, new, cb_args):
        self.log("Automatik-Schalter hat gewechselt von %s nach %s", old, new)
        self.reagiere_auf_automatik(new)

    def reagiere_auf_automatik(self, auto_state):
        if auto_state == "off":
            self.log("Schalte Automatik aus!")
            if self.temp_listen_handle is not None:
                self.cancel_listen_state(self.temp_listen_handle)
            self.aktiv = None
        else:
            self.log("Schalte Automatik ein!")
            akt_t = self.get_state(self.thermometer_name)
            self.reagiere_auf_temperatur(akt_t)                                                                             

            # Wir wollen mitbekommen, wenn die Temperatur wechselt 
            self.temp_listen_handle = self.listen_state(self.temperatur_callback, self.thermometer_name)

    def luefter_ein(self):
        #self.log("Schalte Luefter ein!")
        if self.aktiv is True:
             self.log("War schon aktiv!")
        else:
             self.log("Schalte Lüfter ein!")
             self.turn_on(self.luefter_name)
             self.aktiv = True

    def luefter_aus(self):
        #self.log("Schalte Luefter aus!")
        if self.aktiv is not False:
            self.log("Schalte Lüfter aus!")
            self.turn_off(self.luefter_name)
            self.aktiv = False
        else:
            self.log("War schon aus!")

    def temperatur_callback(self, entity, attribute, old, new, cb_args):
        self.log("Temperatur %s wechselte von %s auf %s °C", self.thermometer_name, old, new)
        self.reagiere_auf_temperatur(new)

    def reagiere_auf_temperatur(self, t):
        try:
            t = float(t)
        except:
            self.log("Temperatur ist nicht auslesbar: %s", t)
            return
        if t > self.start_temp:
            self.luefter_ein()
        elif t <= self.stop_temp:
            self.luefter_aus()
