[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# SmartThings WindFree

A Home Assistant custom integration extending the official SmartThings integration
with Samsung WindFree AC capabilities.

Forked from the official `homeassistant/components/smartthings` integration
(HA 2025.6.x) and the now-unmaintained veista/custom integration.

## Features Beyond Official Integration

- **`disabledCapabilities` fix**: Overrides `KEEP_CAPABILITY_QUIRK` to always preserve
  WindFree AC capabilities (beep, display, power, air quality, dust) that Samsung
  marks as disabled on ARTIK051 devices. The official integration strips these
  capabilities because their attribute values are `None`.
- **Quiet preset workaround**: Forces "quiet" mode for ARTIK051 models that
  don't report it in supported modes
- **Auto cleaning mode**: Switch entity for `custom.autoCleaningMode`
- **Dust filter reset**: Button entity for `custom.dustFilter`
- **Audio feedback volume**: Select entity for `samsungce.airConditionerAudioFeedback`

## Features Restored by `disabledCapabilities` Fix

These capabilities have code in the official integration but don't work on
ARTIK051 WindFree ACs because Samsung lists them in `disabledCapabilities`:

- Display ON/OFF switch (`samsungce.airConditionerLighting`)
- Beep ON/OFF switch (`samsungce.airConditionerBeep`)
- Power consumption sensor (`powerConsumptionReport`)
- Air quality, dust, fine dust sensors

Our fork restores these by making `KEEP_CAPABILITY_QUIRK` unconditional for
WindFree AC capabilities.

## Migration from veista/custom

1. Remove veista/custom from HACS
2. Delete the veista/custom config entry from HA
3. Disable or delete ghost entities (unavailable sensors from old integration)
4. Install this integration via HACS
5. Set up SmartThings integration (OAuth2 flow)

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS
2. Search for "SmartThings WindFree"
3. Install
4. Restart Home Assistant

### Manual

1. Copy `custom_components/smartthings/` to your HA config directory
2. Restart Home Assistant

## Configuration

Same as official SmartThings integration: Settings → Devices & Services → Add Integration → SmartThings WindFree

## Supported Devices

Tested on Samsung WindFree ACs (model ARTIK051_PRAC_20K).
Should work with other Samsung AC models that expose the relevant capabilities.