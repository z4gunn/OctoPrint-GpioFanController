# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero import PWMLED

class GpiofancontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin,
							  octoprint.plugin.SimpleApiPlugin):

	def __init__(self):
		self.fan = None

	
	def init_fan(self, pin, frequency):
		try:
			self.fan = PWMLED(pin=pin, initial_value=0, frequency=frequency)
			self._logger.info("GPIO FAN Controller Initialized")
		except:
			self._logger.error("Error occured while initializing GPIO FAN Controller")


	def on_after_startup(self):
		pin = self._settings.get_int(["pin"])
		freq = self._settings.get_int(["freq"])
		if(pin is not None and freq is not None):
			self.init_fan(pin, freq)


	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)


	def get_settings_defaults(self):
		return dict(
			pin=17,
			freq=100,
		)


	def get_assets(self):
		return dict(
			js=["js/gpiofancontroller.js"],
			css=["css/gpiofancontroller.css"],
			less=["less/gpiofancontroller.less"]
		)


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
		]

	def get_api_commands(self):
		return dict(update_speed=["speed"])

	def on_api_command(self, command, data):
		if command == "update_speed":
			speedStr = data.get('speed', None)
			if speedStr != None:
				speed = float(speedStr)
				if speed != None:
					self.fan.value = speed

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			gpiofancontroller=dict(
				displayName="Gpiofancontroller Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="z4gunn",
				repo="OctoPrint-GpioFanController",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/z4gunn/OctoPrint-GpioFanController/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "GPIO FAN Controller"

#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = GpiofancontrollerPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

