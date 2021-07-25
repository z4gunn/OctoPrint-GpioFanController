# OctoPrint-GpioFanController

This is a lightweight plugin dedicated for controlling a fan via Raspberry Pi GPIO pin.  This plugin has the following features:

* Convenient sidebar control
* Adjustable FAN speed
* Pin selection via settings
* M106 / M107 GCODE support
* Independent GCODE control using optional fan index
* Optional proportional speed mode based on CPU temperature


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/z4gunn/OctoPrint-GpioFanController/archive/master.zip


## IMPORTANT - FAN Compatibility

This plugin is only intended to drive an external brushless DC FAN via MOSFET driver circuit.  A MOSFET must be used to drive the FAN since the PI is not capable of providing adequate current to the FAN.  

It is a also a good idea to use a separate power supply to drive the FAN since the PI power supply might not have adequate current to drive the PI + FAN.  The following diagram is an example of how to interface to a 12V DC FAN.


![Wiring Diagram](/docs/imgs/wiring_diagram.png)