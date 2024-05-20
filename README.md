# MIDI to MQTT Service

This repository contains a Python script that receives MIDI events and sends them to an MQTT broker. The script is designed to run on a Raspberry Pi and can be set up to start on boot using `systemd`.

## Requirements

Ensure you have the required Python packages installed:

- `paho-mqtt`
- `rtmidi-python`

### Installation of Dependencies

1. **paho-mqtt** :

```sh
sudo apt update
sudo apt install python3-paho-mqtt
```

2. **rtmidi-python** (if available):

```sh
sudo apt install python3-rtmidi
```

3. **Run the Script** :

```sh
python3 midi2mqtt.py --host 192.168.4.221 --port 1883 --topicprefix homeassistant --midiport 2
```

### Command Line Arguments

- `--host`: Host of the MQTT Broker (default: `localhost`)
- `--port`: Port of the MQTT Broker (default: `1883`)
- `--midiport`: Port of the MIDI Interface (default: `1`)
- `--topicprefix`: Prefix for the MQTT topic (default: `midi`)

### Usage Example

To subscribe to the MQTT messages published by this script, use a client like `mosquitto_sub`:

```sh
mosquitto_sub -h localhost -t "midi/#" -v
```

### Logging

The script logs important events and errors. Ensure to check the logs for connection status and any issues that may arise.

## Setup as a Systemd Service

1. **Create a service file** :

```sh
sudo nano /etc/systemd/system/midi2mqtt.service
```

2. **Add the following content to the service file** :

```ini
[Unit]
Description=MIDI to MQTT Service
After=network.target

[Service]
ExecStartPre=/bin/sleep 30
ExecStart=/usr/bin/python3 /home/pi/midi2mqtt2ha/midi2mqtt.py --host 192.168.4.221 --port 1883 --topicprefix homeassistant --midiport 2
WorkingDirectory=/home/pi/midi2mqtt2ha
StandardOutput=journal
StandardError=journal
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

3. **Reload the systemd daemon** :

```sh
sudo systemctl daemon-reload
```

4. **Enable the service to start on boot** :

```sh
sudo systemctl enable midi2mqtt.service
```

5. **Start the service** :

```sh
sudo systemctl start midi2mqtt.service
```

6. **Check the status of the service** :

```sh
sudo systemctl status midi2mqtt.service
```

This setup will ensure that your script runs on startup and waits for 30 seconds before starting.

This guide will walk you through setting up `midi2mqtt.py` to run automatically at boot on a MacOS system using a launchd plist file. This method ensures that the script starts without manual intervention, making your setup more robust and user-friendly.

## Step 1: Creating a plist file

First, we need to create a plist file that macOS will use to understand how to run our script at boot. You can do this by running the following command in the Terminal. This command creates a plist file with the necessary configuration to run `midi2mqtt.py` automatically.

```bash
cat << EOF > ~/Library/LaunchAgents/com.midi2mqtt.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.midi2mqtt</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/chase/Code/midi2mqtt2ha/midi2mqtt.py</string>
        <string>--host</string>
        <string>192.168.4.221</string>
        <string>--port</string>
        <string>1883</string>
        <string>--topicprefix</string>
        <string>homeassistant</string>
        <string>--midiport</string>
        <string>2</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
```

**Note:** The final argument `pwd` in the original instructions appears to be misplaced and is not included here. Ensure all arguments are correctly specified for your setup.

## Step 2: Loading the plist file

After creating the plist file, you'll need to load it to schedule your script to run at boot. Execute the following command to achieve this:

```bash
launchctl load ~/Library/LaunchAgents/com.midi2mqtt.plist
```

## Modifying the Script

You're encouraged to keep any script modifications or additional files within the `midi2mqtt2ha` directory for organization. Just make sure the `midi2mqtt.py` script has the appropriate permissions to access and modify these files as necessary.

## Troubleshooting

- If your script does not run as expected, check the permissions of `midi2mqtt.py` and ensure it's executable.
- Use `launchctl list | grep midi2mqtt` to check if your plist is loaded and to see any status codes that might indicate errors.

## Conclusion

You've now set up `midi2mqtt.py` to run at boot on your MacOS system. This setup ensures that your system is always ready to go without needing manual script starts. Feel free to modify the script as per your requirements, keeping the modifications within the specified directory for ease of management.---
