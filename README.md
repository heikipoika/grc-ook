# grc-ook
Gnu radio implementation to modulate and demodulate On Off Keyed (OOK) packet transmissions.


This flowchart is made for the Pluto SDR, which provides both Rx and Tx. It is intended to be tuned to 433.92MHz in order to receive and send data.

Other SDRs may be used, remove the Sink part in order to just decode messages.

Currently there is no autodetection for:

* Bitrate. The XXX-rate Variable needs to be set manually to the length of a short pulse. Use a QT GUI Time Sink to measure....

* ASK modulation scheme. It demodulates pulse width modulation with fixed period or fixed gap only (not fixed pulse variable gap such as the Nexa system). It modulates with fixed period but that can easily be changed to fixed gap (and even fixed pulse variable gap).

* Threshold. It may be adjusted manually to fit the antenna and the current noise floor level. The Rx and Tx attenuation may also be adjusted for the required transmission range.

The current design listens to its own transmissions (unless the antenna setup provides enough isolation). For a full duplex comms link, the Rx Tx frequencies may be separeted, but for a half duplex link a Rx/Tx switch may be added.

Disclaimer:
Do not active Tx unless you know what you are doing and have the required permits etc.
