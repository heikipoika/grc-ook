# grc-ook
Gnu radio implementation to modulate and demodulate On Off Keyed (OOK) packet transmissions, which is the simplest form of Amplitude Shift Keying (ASK) modulation.

![Oscilloscope dump](/images/screenshot.png)

This flowchart is made for the Pluto SDR, which provides both Rx and Tx. It is intended to be tuned to 433.92MHz in order to receive and send data. Note: The Pluto supplied antennas do not work very well on 433Mhz so you need to connect something else.

Other SDRs may be used, remove the Sink part if the SDR only supports Rx.

## Limitataions

Currently there is no autodetection for:

* Bitrate. The *short_pulse* variable needs to be set manually to the length of a short pulse. Use a QT GUI Time Sink to measure....

* ASK modulation scheme. It demodulates pulse width modulation with fixed period or fixed gap only (not fixed pulse variable gap such as the Nexa system). It modulates with fixed period but that can easily be changed to fixed gap (and even fixed pulse variable gap).

* Threshold. They may be adjusted manually to fit the antenna and the current noise floor level. The Rx and Tx attenuation may also be adjusted for the required transmission range.

## Intended use

This is not meant as a complete tool, but its components can be used to:

* Sniff short distance radio tranmission of simple devices such as thermometers and switches etc, and mimic their behaviour. Protocol details for some known devices can be found here: https://github.com/merbanan/rtl_433/tree/master/src/devices in order to be able to encode/decode the actual content of existing devices messages.

* Set up a simple comms link between two devices. The current design will listen to its own transmissions (unless the antenna setup provides enough isolation). A simple Rx/Tx switch may be added to the flowchart (half duplex link). For a full duplex link, the Rx Tx frequencies may be separeted.

## Disclaimer

Do not active Tx unless you know what you are doing and have the required permits etc.
