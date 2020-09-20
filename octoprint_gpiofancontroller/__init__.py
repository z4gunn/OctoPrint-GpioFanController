# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero import PWMLED

class GpiofancontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self.fan = None

	
	def init_fan(self, pin, frequency):
		try:
			self.fan = PWMLED(pin=pin, initial_value=0, frequency=frequency)
			self._logger.info("FAN Initialized")
		except:
			self._logger.error("Error occured while initializing FAN")


	def on_after_startup(self):
		pin = self._settings.get_int(["pin"])
		freq = self._settings.get_int(["freq"])
		speed = self._settings.get_float(["speed"])
		self._logger.info("Pin #: %s" % pin)
		self._logger.info("Freq:   %s" % freq)
		self._logger.info("Speed:  %s" % speed)
		if(pin is not None and freq is not None):
			self.init_fan(pin, freq)


	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		speed = self._settings.get_float(["speed"])
		self._logger.info("Settings Saved")
		self._logger.info("Speed : " + str(speed))
		self.fan.value = speed
		

	def get_settings_defaults(self):
		return dict(
			pin=17,
			freq=100,
			speed = 0.0,
		)


	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/gpiofancontroller.js"],
			css=["css/gpiofancontroller.css"],
			less=["less/gpiofancontroller.less"]
		)


	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]


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


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "GPIO FAN Controller"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
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

