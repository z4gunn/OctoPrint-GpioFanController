/*
 * View model for OctoPrint-GpioFanController
 *
 * Author: Erik Gundersen
 * License: AGPLv3
 */
$(function() {
    function GpiofancontrollerViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
        self.speed = ko.observable(0.0);

        self.onUpdateSpeed = function(element, event) {
            var newSpeed = event.currentTarget.value
            if(newSpeed) {
                self.speed(newSpeed)
                OctoPrint.simpleApiCommand('gpiofancontroller', 'update_speed', {'speed': newSpeed})
            }
        }
    
        self.onBeforeBinding = function() {
            //self.speed(self.settings.settings.plugins.gpiofancontroller.speed());      
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: GpiofancontrollerViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#sidebar_plugin_gpiofancontroller"]
    });
});
