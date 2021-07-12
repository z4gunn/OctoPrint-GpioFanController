# OctoPrint-GpioFanController

This is a lightweight plugin dedicated for controlling a fan via Raspberry Pi GPIO pin.  This plugin has the following features:

* Convenient sidebar control
* Adjustable FAN speed
* Pin selection via settings
* M106 / M107 GCODE support
* Independent GCODE control using optional fan index


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/z4gunn/OctoPrint-GpioFanController/archive/master.zip


## IMPORTANT - FAN Compatibility

This plugin is only intended to drive an external brushless DC FAN via MOSFET driver circuit.  A MOSFET must be used to drive the FAN since the PI is not capable of providing adequate current to the FAN.  

This is a great [tutorial](https://create.arduino.cc/projecthub/ejshea/connecting-an-n-channel-mosfet-7e0242) that explains on how to connect a brushless DC FAN to the an Arduino, however the same concept applies to interfacing to a PI.  You can also use a larger MOSFET such as [IRLB8721](https://www.adafruit.com/product/355) to drive fans that require more than  200 mA.