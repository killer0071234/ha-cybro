# ha-cybro

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]][forum]

## Functionality

This integration is a local / remote polling integration that connects to a running cybro-scgi-server from Cybrotech. To use this integration you need to have a running scgi server (it could be a docker container or native installed).

### binary_sensor

There are some diagnostic binary sensors exposed:

- general_error -> the general error tag from the PLC device
- retentive_fail -> the retentive error tag from the PLC device
- scan_overrun -> the scan overrun tag from the PLC device, which indicates a program overrun

### sensor

There are some diagnostic binary sensors exposed:

- scan_time -> scan time in ms from the PLC program
- scan_time_max -> maximum scan time in ms from the PLC program
- sys.ip_port -> ip addres of the PLC device

#### Common Attributes

| Attribute   | Example Values (comma separated)  |
| ----------- | --------------------------------- |
| description | the description text from the PLC |

### Devices

A device is created for each PLC.

{% if not installed %}

## Installation

### HACS

1. Install [HACS](https://hacs.xyz/)
2. Go to HACS "Integrations >" section
3. In the lower right click "+ Explore & Download repositories"
4. Search for "Cybro" and add it
   - HA Restart is not needed since it is configured in UI config flow
5. In the Home Assistant (HA) UI go to "Configuration"
6. Click "Integrations"
7. Click "+ Add Integration"
8. Search for "Cybro"

### Manual

1. Using the tool of choice open the directory (folder) for your [HA configuration](https://www.home-assistant.io/docs/configuration/) (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `cybro`.
4. Download _all_ the files from the `custom_components/cybro/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the Home Assistant (HA) UI go to "Configuration"
8. Click "Integrations"
9. Click "+ Add Integration"
10. Search for "Cybro"

{% endif %}

## Configuration (Important! Please Read)

Config is done in the HA integrations UI.

### Disable new entities

If you prefer new entities to be disabled by default:

1. In the Home Assistant (HA) UI go to "Configuration"
2. Click "Integrations"
3. Click the three dots in the bottom right corner for the Cybro integration
4. Click "System options"
5. Disable "Enable newly added entities"

## Tested Devices

- Cybro-2
- Cybro-3

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](https://github.com/killer0071234/ha-cybro/blob/master/CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/killer0071234/ha-cybro.svg?style=for-the-badge
[commits]: https://github.com/killer0071234/ha-cybro/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/killer0071234/ha-cybro.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%killer0071234-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/killer0071234/ha-cybro.svg?style=for-the-badge
[releases]: https://github.com/killer0071234/ha-cybro/releases
[user_profile]: https://github.com/killer0071234
