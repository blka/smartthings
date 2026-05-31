"""Diagnostic script to query SmartThings API for a device's full status.

This script reads the OAuth token from the HA config and queries the
SmartThings API directly to see the raw device capabilities, including
which are disabled and what attribute values they report.

Usage:
    python3 diagnose_device.py [--device-id DEVICE_ID]

The token is read from the HA config entry storage file.
Requires: pysmartthings, aiohttp
"""

import asyncio
import json
import os
import sys

from pysmartthings import SmartThings


async def main():
    device_id = "68b9468505c2d32980a389d95b1759b3"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--device-id" and len(sys.argv) > 2:
            device_id = sys.argv[2]
        else:
            device_id = sys.argv[1]

    # Try to find the token from HA config
    token = None

    # Check environment variable first
    token = os.environ.get("SMARTTHINGS_TOKEN")

    if not token:
        # Try to read from HA config
        ha_config_paths = [
            "/config/.storage/core.config_entries",
            "/homeassistant/.storage/core.config_entries",
            "/home/homeassistant/.storage/core.config_entries",
        ]
        for path in ha_config_paths:
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                for entry in data.get("data", {}).get("entries", []):
                    if entry.get("domain") == "smartthings":
                        token = entry.get("data", {}).get("token")
                        if token:
                            break
            if token:
                break

    if not token:
        print("=" * 60)
        print("ERROR: No SmartThings token found.")
        print("")
        print("Set the SMARTTHINGS_TOKEN environment variable:")
        print("  export SMARTTHINGS_TOKEN=your_token_here")
        print("  python3 diagnose_device.py")
        print("")
        print("Or get a token from:")
        print("  https://account.smartthings.com/tokens")
        print("=" * 60)
        sys.exit(1)

    client = SmartThings(token=token)

    print(f"Querying device: {device_id}")
    print("=" * 60)

    # Get raw device info
    try:
        device_info = await client.get_raw_device(device_id)
        print("\n### Device Info ###")
        print(f"  Name: {device_info.get('name', 'N/A')}")
        print(f"  Label: {device_info.get('label', 'N/A')}")
        print(f"  Type: {device_info.get('type', 'N/A')}")
        print(f"  Device ID: {device_info.get('deviceId', 'N/A')}")

        # Print components and their categories
        for comp_name, comp in device_info.get("components", {}).items():
            categories = comp.get("categories", [])
            print(f"  Component '{comp_name}': categories={categories}")

    except Exception as e:
        print(f"Error getting device info: {e}")
        # Try to continue with status only

    # Get raw device status
    try:
        status = await client.get_raw_device_status(device_id)
        print("\n### Device Status ###")

        components = status.get("components", {})

        for comp_name, comp_status in components.items():
            print(f"\n  Component: {comp_name}")
            for cap_id, cap_data in comp_status.items():
                print(f"\n    Capability: {cap_id}")

                # Check for disabled capabilities
                if cap_id == "custom.disabledCapabilities":
                    disabled = cap_data.get("disabledCapabilities", {}).get("value", [])
                    print(f"      >>> DISABLED CAPABILITIES: {disabled}")

                # Print all attributes
                for attr_name, attr_data in cap_data.items():
                    if isinstance(attr_data, dict):
                        value = attr_data.get("value")
                        unit = attr_data.get("unit", "")
                        data_type = attr_data.get("data", None)
                        if data_type is not None:
                            print(f"      {attr_name}: value={value}, unit={unit}, data={data_type}")
                        else:
                            print(f"      {attr_name}: value={value}, unit={unit}")
                    else:
                        print(f"      {attr_name}: {attr_data}")

    except Exception as e:
        print(f"Error getting device status: {e}")

    print("\n" + "=" * 60)
    print("Diagnostic complete.")


if __name__ == "__main__":
    asyncio.run(main())