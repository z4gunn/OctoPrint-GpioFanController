# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
from gpiozero.pins.rpigpio import RPiGPIOFactory
from gpiozero import PWMLED
import os

CPU_FAN_UPDATE_INTERVAL = 5
CPU_FAN_TEMP_MIN_DEFAULT = 50
CPU_FAN_TEMP_MAX_DEFAULT = 70
CPU_FAN_TEMP_HYST_DEFAULT = 3
CPU_FAN_SPEED_MIN_DEFAULT = 40
CPU_FAN_SPEED_MAX_DEFAULT = 100

class GpiofancontrollerPlugin(octoprint.plugin.StartupPlugin,
							  octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.TemplatePlugin,
							  octoprint.plugin.SimpleApiPlugin,
							  octoprint.plugin.ShutdownPlugin):

	def __init__(self):
		self.fan = None
		self.speed = 0.0
		self.gcode_command_enable = False
		self.gcode_index_enable = False
		self.gcode_fan_index = 4
		self.pin_factory = RPiGPIOFactory()
		self.cpu_fan_timer = None
		self.cpu_fan_enable = False
		self.cpu_fan_temp_min = CPU_FAN_TEMP_MIN_DEFAULT
		self.cpu_fan_temp_max = CPU_FAN_TEMP_MAX_DEFAULT
		self.cpu_fan_temp_hyst = CPU_FAN_TEMP_HYST_DEFAULT
		self.cpu_fan_speed_min = CPU_FAN_SPEED_MIN_DEFAULT
		self.cpu_fan_speed_max = CPU_FAN_SPEED_MAX_DEFAULT


	def init_fan(self, pin, frequency, speed):
		try:
			self.deinit_fan()
			self.fan = PWMLED(pin=pin, initial_value=speed, frequency=frequency, pin_factory=self.pin_factory)
			self._logger.info("PWM pin initialized with pin factory: " + str(self.fan.pin_factory))
		except:
			self._logger.error("Error occurred while initializing PWM pin")


	def deinit_fan(self):
		try:
			if self.fan is not None:
				self.fan.close()
				self.fan = None
				self._logger.info("PWM pin deinitialized")
		except:
			self._logger.error("Error occurred while deinitializing PWM pin")


	def start_cpu_fan_timer(self):
		try:
			self.stop_cpu_fan_timer()
			if self.cpu_fan_enable:
				self.cpu_fan_timer = octoprint.util.RepeatedTimer(CPU_FAN_UPDATE_INTERVAL, self.update_cpu_fan_speed, run_first=True,)
				self.cpu_fan_timer.start()
				self._logger.info("CPU fan update timer started")
		except:
			self._logger.error("Error occurred while starting cpu fan update timer")


	def stop_cpu_fan_timer(self):
		try:
			if self.cpu_fan_timer is not None:
				self.cpu_fan_timer.cancel()
				self.cpu_fan_timer = None
				self._logger.info("CPU fan update timer stopped")
		except:
			self._logger.error("Error occurred while stopping cpu fan update timer")


	def update_fan_speed(self, speed):
		self._logger.info("New Fan Speed: " + str(speed))
		if self.fan is not None and speed >= 0.0 and speed <= 1.0:
			self.speed = speed
			self.fan.value = self.speed
			

	def on_after_startup(self):
		pin = self._settings.get_int(["pin"])
		freq = self._settings.get_int(["freq"])
		if pin is not None and freq is not None and self.speed is not None:
			self.init_fan(pin, freq, self.speed)
		gcode_command_enable = self._settings.get_boolean(["gcode_command_enable"])
		if gcode_command_enable is not None:
			self.gcode_command_enable = gcode_command_enable
		gcode_index_enable = self._settings.get_boolean(["gcode_index_enable"])
		if gcode_index_enable is not None:
			self.gcode_index_enable = gcode_index_enable
		gcode_fan_index = self._settings.get_int(["gcode_fan_index"])
		if gcode_fan_index is not None:
			self.gcode_fan_index = gcode_fan_index
		cpu_fan_enable = self._settings.get_boolean(["cpu_fan_enable"])
		if cpu_fan_enable is not None:
			self.cpu_fan_enable = cpu_fan_enable
		cpu_fan_temp_min = self._settings.get_int(["cpu_fan_temp_min"])
		if cpu_fan_temp_min is not None:
			self.cpu_fan_temp_min = cpu_fan_temp_min
		cpu_fan_temp_max = self._settings.get_int(["cpu_fan_temp_max"])
		if cpu_fan_temp_max is not None:
			self.cpu_fan_temp_max = cpu_fan_temp_max
		cpu_fan_temp_hyst = self._settings.get_int(["cpu_fan_temp_hyst"])
		if cpu_fan_temp_hyst is not None:
			self.cpu_fan_temp_hyst = cpu_fan_temp_hyst
		cpu_fan_speed_min = self._settings.get_int(["cpu_fan_speed_min"])
		if cpu_fan_speed_min is not None:
			self.cpu_fan_speed_min = cpu_fan_speed_min
		cpu_fan_speed_max = self._settings.get_int(["cpu_fan_speed_max"])
		if cpu_fan_speed_max is not None:
			self.cpu_fan_speed_max = cpu_fan_speed_max
		self.start_cpu_fan_timer()


	def on_shutdown(self):
		self.stop_cpu_fan_timer()
		self.deinit_fan()


	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		pin = self._settings.get_int(["pin"])
		freq = self._settings.get_int(["freq"])
		if pin is not None and freq is not None and self.speed is not None:
			self.init_fan(pin, freq, self.speed)
		else:
			self._logger.error("Error occurred while initializing PWM pin")
		gcode_command_enable = self._settings.get_boolean(["gcode_command_enable"])
		if gcode_command_enable is not None:
			self.gcode_command_enable = gcode_command_enable
		gcode_index_enable = self._settings.get_boolean(["gcode_index_enable"])
		if gcode_index_enable is not None:
			self.gcode_index_enable = gcode_index_enable
		gcode_fan_index = self._settings.get_int(["gcode_fan_index"])
		if gcode_fan_index is not None:
			self.gcode_fan_index = gcode_fan_index
		cpu_fan_enable = self._settings.get_boolean(["cpu_fan_enable"])
		if cpu_fan_enable is not None:
			self.cpu_fan_enable = cpu_fan_enable
		cpu_fan_temp_min = self._settings.get_int(["cpu_fan_temp_min"])
		if cpu_fan_temp_min is not None:
			self.cpu_fan_temp_min = cpu_fan_temp_min
		cpu_fan_temp_max = self._settings.get_int(["cpu_fan_temp_max"])
		if cpu_fan_temp_max is not None:
			self.cpu_fan_temp_max = cpu_fan_temp_max
		cpu_fan_temp_hyst = self._settings.get_int(["cpu_fan_temp_hyst"])
		if cpu_fan_temp_hyst is not None:
			self.cpu_fan_temp_hyst = cpu_fan_temp_hyst
		cpu_fan_speed_min = self._settings.get_int(["cpu_fan_speed_min"])
		if cpu_fan_speed_min is not None:
			self.cpu_fan_speed_min = cpu_fan_speed_min
		cpu_fan_speed_max = self._settings.get_int(["cpu_fan_speed_max"])
		if cpu_fan_speed_max is not None:
			self.cpu_fan_speed_max = cpu_fan_speed_max
		self.start_cpu_fan_timer()
		
		
	def get_settings_defaults(self):
		return dict(
			pin=17,
			freq=100,
			gcode_command_enable=False,
			gcode_index_enable=False,
			gcode_fan_index=4,
			cpu_fan_enable=False,
			cpu_fan_temp_min=CPU_FAN_TEMP_MIN_DEFAULT,
			cpu_fan_temp_max=CPU_FAN_TEMP_MAX_DEFAULT,
			cpu_fan_temp_hyst=CPU_FAN_TEMP_HYST_DEFAULT,
			cpu_fan_speed_min=CPU_FAN_SPEED_MIN_DEFAULT,
			cpu_fan_speed_max=CPU_FAN_SPEED_MAX_DEFAULT,
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
				if speed is not None:
					self.update_fan_speed(speed)


	def gcode_parse_speed(self, cmd):
		params = cmd.split("S")
		if len(params) != 2:
			return None
		else:
			try:
				speed = int(params[1].split()[0])
				if speed < 0 or speed > 255:
					return None
				else:
					return speed / 255
			except:
				return None


	def gcode_parse_index(self, cmd):
		params = cmd.split("P")
		if len(params) != 2:
			return None
		else:
			try:
				index = int(params[1].split()[0])
				if index > 0:
					return index
				else:
					return None
			except:
				return None
            

	def on_gcode_command(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if not self.gcode_command_enable:
			return 
		if gcode and gcode.startswith("M106"):
			speed = self.gcode_parse_speed(cmd)
			if self.gcode_index_enable:
				index = self.gcode_parse_index(cmd)
				if index is not None and speed is not None: 
					if index == self.gcode_fan_index:
						self.update_fan_speed(speed)
			else:
				if speed is not None:
					self.update_fan_speed(speed)
			
		elif gcode and gcode.startswith("M107"):
			if self.gcode_index_enable:
				index = self.gcode_parse_index(cmd)
				if index is not None: 
					if index == self.gcode_fan_index:
						self.update_fan_speed(0.0)
			else:
				self.update_fan_speed(0.0)
		self._plugin_manager.send_plugin_message(self._identifier, dict(speed=self.speed))


	def update_cpu_fan_speed(self):
		try:
			res = os.popen('vcgencmd measure_temp').readline()
			new_temp = float(res.replace("temp=","").replace("'C\n",""))
			self._logger.info("New CPU Temp: " + str(new_temp))

			new_speed = self.speed
			if new_temp > self.cpu_fan_temp_max:
				new_speed = float(self.cpu_fan_speed_max) / 100.0
			elif new_temp < self.cpu_fan_temp_min:
				new_speed = 0.0
			else:
				speed_range = (float(self.cpu_fan_speed_max) / 100.0) - (float(self.cpu_fan_speed_min) / 100.0)
				temp_range = float(self.cpu_fan_temp_max) - float(self.cpu_fan_temp_min)
				slope = speed_range / temp_range
				y_int = (float(self.cpu_fan_speed_max) / 100.0) - slope * float(self.cpu_fan_temp_max)
				new_speed = slope * new_temp + y_int

			self.update_fan_speed(new_speed)
			self._plugin_manager.send_plugin_message(self._identifier, dict(speed=self.speed))
		
		except:
			self._logger.error("Error occurred while updating CPU fan speed")


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
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.sent": __plugin_implementation__.on_gcode_command,
	}

