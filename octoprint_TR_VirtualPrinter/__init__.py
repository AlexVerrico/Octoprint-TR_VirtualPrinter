# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2015 The OctoPrint Project - Released under terms of the AGPLv3 License"

import octoprint.plugin


class TR_VirtualPrinterPlugin(
    octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin
):
    def get_template_configs(self):
        return [{"type": "settings", "custom_bindings": False}]

    def get_settings_defaults(self):
        return {
            "enabled": False,
            "okAfterResend": False,
            "forceChecksum": False,
            "numExtruders": 1,
            "pinnedExtruders": None,
            "includeCurrentToolInTemps": True,
            "includeFilenameInOpened": True,
            "hasBed": True,
            "hasChamber": False,
            "repetierStyleTargetTemperature": False,
            "okBeforeCommandOutput": False,
            "smoothieTemperatureReporting": False,
            "klipperTemperatureReporting": False,
            "reprapfwM114": False,
            "sdFiles": {"size": True, "longname": False},
            "throttle": 0.01,
            "sendWait": True,
            "waitInterval": 1.0,
            "rxBuffer": 64,
            "commandBuffer": 4,
            "supportM112": True,
            "echoOnM117": True,
            "brokenM29": True,
            "brokenResend": False,
            "supportF": False,
            "firmwareName": "Virtual Marlin 1.0",
            "sharedNozzle": False,
            "sendBusy": False,
            "busyInterval": 2.0,
            "simulateReset": True,
            "resetLines": ["start", "Marlin: Virtual Marlin!", "\x80", "SD card ok"],
            "preparedOks": [],
            "okFormatString": "ok",
            "m115FormatString": "FIRMWARE_NAME:{firmware_name} PROTOCOL_VERSION:1.0",
            "m115ReportCapabilities": True,
            "capabilities": {
                "AUTOREPORT_TEMP": True,
                "AUTOREPORT_SD_STATUS": True,
                "EMERGENCY_PARSER": True,
            },
            "m114FormatString": "X:{x} Y:{y} Z:{z} E:{e[current]} Count: A:{a} B:{b} C:{c}",
            "m105TargetFormatString": "{heater}:{actual:.2f}/ {target:.2f}",
            "m105NoTargetFormatString": "{heater}:{actual:.2f}",
            "ambientTemperature": 21.3,
            "errors": {
                "checksum_mismatch": "Checksum mismatch",
                "checksum_missing": "Missing checksum",
                "lineno_mismatch": "expected line {} got {}",
                "lineno_missing": "No Line Number with checksum, Last Line: {}",
                "maxtemp": "MAXTEMP triggered!",
                "mintemp": "MINTEMP triggered!",
                "command_unknown": "Unknown command {}",
            },
            "enable_eeprom": True,
            "support_M503": True,
            "resend_ratio": 0,
        }

    def get_settings_version(self):
        return 1

    def on_settings_migrate(self, target, current):
        if current is None:
            config = self._settings.global_get(["devel", "TR_VirtualPrinter"])
            if config:
                self._logger.info(
                    "Migrating settings from devel.TR_VirtualPrinter to plugins.TR_VirtualPrinter..."
                )
                self._settings.global_set(
                    ["plugins", "TR_VirtualPrinter"], config, force=True
                )
                self._settings.global_remove(["devel", "TR_VirtualPrinter"])

    def virtual_printer_factory(self, comm_instance, port, baudrate, read_timeout):
        if not port == "VIRTUAL1":
            return None

        if not self._settings.get_boolean(["enabled"]):
            return None

        import logging.handlers

        from octoprint.logging.handlers import CleaningTimedRotatingFileHandler

        seriallog_handler = CleaningTimedRotatingFileHandler(
            self._settings.get_plugin_logfile_path(postfix="serial"),
            when="D",
            backupCount=3,
        )
        seriallog_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        seriallog_handler.setLevel(logging.DEBUG)

        from . import virtual

        serial_obj = virtual.TR_VirtualPrinter(
            self._settings,
            data_folder=self.get_plugin_data_folder(),
            seriallog_handler=seriallog_handler,
            read_timeout=float(read_timeout),
            faked_baudrate=baudrate,
        )
        return serial_obj

    def get_additional_port_names(self, *args, **kwargs):
        if self._settings.get_boolean(["enabled"]):
            return ["VIRTUAL1"]
        else:
            return []


__plugin_name__ = "Modified Virtual Printer"
__plugin_author__ = "Alex Verrico, heavily based on work by Gina Häußge and Daid Braam"
__plugin_homepage__ = (
    "https://github.com/AlexVerrico/Octoprint-TR_VirtualPrinter"
)
__plugin_license__ = "AGPLv3"
__plugin_description__ = "Provides a virtual printer via a virtual serial port for development and testing purposes"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    plugin = TR_VirtualPrinterPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.transport.serial.factory": plugin.virtual_printer_factory,
        "octoprint.comm.transport.serial.additional_port_names": plugin.get_additional_port_names,
    }
