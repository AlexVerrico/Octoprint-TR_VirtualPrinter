# OctoPrint-Tr_VirtualPrinter

### This plugin is provided as-is. It works for me, so I consider it finished. If it doesn't work for you, feel free to open a polite issue, but don't _expect_ a response

A modified Virtual Printer for Octoprint.
Originally built by Gina Häußge based on work by Daid Braam.

See [https://docs.octoprint.org/en/1.6.1/development/virtual_printer.html](https://docs.octoprint.org/en/1.6.1/development/virtual_printer.html) for original commands (all of these are still supported)

Custom commands:

- `override_temp <heater> <temperature>`: set the virtual printer to return `<temperature>` as the temperature for `<heater>`. `<temperature>` must be a valid float
- `rm_override_temp <heater>`: remove the temperature override for `<heater>`

## Setup

Install manually using this URL:

    https://github.com/AlexVerrico/Octoprint-TR_VirtualPrinter/archive/master.zip

## FAQ
- Q: What does the name mean? A: TR = Thermal Runaway. I built this plugin to aid in testing my plugin [Octoprint-ThermalRunaway](https://github.com/AlexVerrico/Octoprint-ThermalRunaway)
- Q: Why isn't this listed on the Octoprint plugin repository? A: I doubt that there is enough demand to warrant it.
- Q: Why havent you added command X? A: Because I don't need it. If you want to add it, open an issue to discuss it.
