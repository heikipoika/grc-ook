# grc-ook
Gnu radio implementation to modulate and demodulate On Off Keyed (OOK) messages


This flowchart is made for the Pluto SDR, which provides both Rx and Tx. It is intended to be tuned to 433.92MHz in order to receive and send data.

Other SDRs may be used, remove the Sink part to just decode messages.

Currently, this design does not autodetect the bitrate. Furthermore it is made for pulse width modulation with fixed period. The XXX-rate Variable needs to be set to the period. You can use a QT GUI Time Sink to measure....

The Threshold may be adjusted to fit the antenna and the current noise floor level. The Rx and Tx attenuation may be adjusted for the required range.

Disclaimer:
Do not active Tx unless you know what you are doing and have the required permits etc.
