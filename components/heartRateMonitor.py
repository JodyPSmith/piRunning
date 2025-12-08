import asyncio
from bleak import BleakClient, BleakScanner

# UUID for the Heart Rate Service
HEART_RATE_SERVICE_UUID = "0000180d-0000-1000-8000-00805f9b34fb"
# UUID for the Heart Rate Measurement Characteristic
HEART_RATE_MEASUREMENT_CHARACTERISTIC_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data):
    """
    Handles incoming heart rate notifications.
    The data format depends on the specific heart rate monitor.
    A common format is a byte array where the second byte is the heart rate.
    """
    heart_rate = int(data[1])
    print(f"Heart Rate: {heart_rate} BPM")

async def run():
    print("Scanning for heart rate monitors...")
    devices = await BleakScanner.discover()
    hr_monitor_address = None

    for device in devices:
        if device.name and "heart" in device.name.lower() or HEART_RATE_SERVICE_UUID in device.metadata.get('uuids', []):
            print(f"Found potential HR monitor: {device.name} ({device.address})")
            hr_monitor_address = device.address
            break

    if not hr_monitor_address:
        print("No heart rate monitor found.")
        return

    print(f"Connecting to {hr_monitor_address}...")
    async with BleakClient(hr_monitor_address) as client:
        if client.is_connected:
            print("Connected!")
            # Enable notifications for the Heart Rate Measurement characteristic
            await client.start_notify(HEART_RATE_MEASUREMENT_CHARACTERISTIC_UUID, notification_handler)
            print("Receiving heart rate data. Press Ctrl+C to stop.")
            while True:
                await asyncio.sleep(1) # Keep the connection alive
        else:
            print("Failed to connect.")

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Disconnected.")