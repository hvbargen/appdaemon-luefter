# appdaemon-luefter
Lüftersteuerung mit AppDaemon für Home Assistant

In der Datei apps.yaml erfolgt die Konfiguration.

Über einen Boolean-Input wird gesteuert, ob die Automatik aktiv ist oder nicht.

Wenn die Automatik aktiv ist, dann ...

... wird der Lüfter gestartet, wenn die Temperatur start_temp überschritten wird
... und gestoppt, wenn die Temperatur stopp_temp unterschritten wird.

Benötigt werden neben den beiden Temperaturen die Namen der Entitäten
für den Automatik-Schalter, für den Tempperatursensor (sprich: Thermometer) und für den Lüfter bzw. dessen Stromversorgung.

Im konkreten Fall ist der Temperatursensor die Temperatur des Inverters 
und der Lüfter ist ein Querstromlüfter, der über ein 12V DC Netzteil an einer Luminea WLAN-Schaltsteckdose hängt.
