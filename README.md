# zenpilot

## Table of Contents

=======================

- [zenpilot](#zenpilot)
  - [Table of Contents](#table-of-contents)
  - [What is zenpilot?](#what-is-zenpilot)
  - [What is openpilot?](#what-is-openpilot)
  - [Community and Contributing](#community-and-contributing)
  - [Safety and Testing](#safety-and-testing)
  - [Directory Structure](#directory-structure)
  - [Licensing](#licensing)

---

## What is zenpilot?

=======================

[zenpilot](https://github.com/chadgauth/zenpilot) is a custom fork of [openpilot](https://github.com/commaai/openpilot).

---

## What is [openpilot](https://github.com/commaai/openpilot)?

=======================

openpilot is an open source driver assistance system that includes features such as Adaptive Cruise Control (ACC), Automated Lane Centering (ALC), Forward Collision Warning (FCW), and Lane Departure Warning (LDW) for a growing number of supported car makes, models, and model years. Also includes a camera-based Driver Monitoring (DM) feature that alerts drivers who may be distracted or asleep.

---

## Community and Contributing

=======================

zenpilot is developed by [chadgauth](https://github.com/chadgauth) and by drivers like you. I welcome both pull requests and issues on [GitHub](http://github.com/chadgauth/zenpilot). Feature requests are encouraged. Bonus points and faster integration if you share commit hashes from other forks. Check out [the contributing docs](docs/CONTRIBUTING.md).

---

## Safety and Testing

=======================

zenpilot will follow all safety/tests guidelines defined in [openpilot safety documentation](https://github.com/commaai/openpilot/docs/SAFETY.md).

---

## Directory Structure

=======================

├── cereal              # The messaging spec and libraries used for logging
├── common              # A collection of developed libraries and functionalities
├── docs                # All documentation related to the project
├── opendbc             # Files for interpreting data from cars
├── panda               # Code for communicating on Controller Area Network (CAN)
├── third_party         # External libraries used in the project
├── pyextra             # Additional Python packages
└── system              # A collection of generic services
    ├── camerad         # Daemon that captures images from camera sensors
    ├── clocksd         # Service that broadcasts current time
    ├── hardware        # Abstraction classes for hardware
    ├── logcatd         # Systemd journal as a service
    └── proclogd        # Service that logs information from /proc
└── selfdrive           # Code necessary for driving the car
    ├── assets          # Assets such as fonts, images, and sounds for the UI
    ├── athena          # Allows communication with the app
    ├── boardd          # Daemon that communicates with the board
    ├── car             # Car-specific code for reading states and controlling actuators
    ├── controls        # Planning and control modules
    ├── debug           # Tools for debugging and car porting
    ├── locationd       # Service for precise localization and vehicle parameter estimation
    ├── loggerd         # Service for logging and uploading car data
    ├── manager         # Daemon that starts and stops all other daemons as needed
    ├── modeld          # Driving and monitoring model runners
    ├── monitoring      # Daemon for determining driver attention
    ├── navd            # Service for turn-by-turn navigation
    ├── sensord         # Interface code for Inertial Measurement Unit (IMU)
    ├── test            # Unit tests, system tests, and a car simulator
    └── ui              # The User Interface

---

## Licensing

=======================

zenpilot is released under the MIT license. Some parts of the software are released under other licenses as specified.

Any user of this software shall indemnify and hold harmless Comma.ai, Inc. and its directors, officers, employees, fork maintainers, agents, stockholders, affiliates, subcontractors and customers from and against all allegations, claims, actions, suits, demands, damages, liabilities, obligations, losses, settlements, judgments, costs and expenses (including without limitation attorneys’ fees and costs) which arise out of, relate to or result from any use of this software by user.

**THIS IS ALPHA QUALITY SOFTWARE FOR RESEARCH PURPOSES ONLY. THIS IS NOT A PRODUCT.
YOU ARE RESPONSIBLE FOR COMPLYING WITH LOCAL LAWS AND REGULATIONS.
NO WARRANTY EXPRESSED OR IMPLIED.**

---
