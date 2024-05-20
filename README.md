# midi2mqtt2ha Setup Guide

### Requirements

Ensure you have the required Python packages installed:

- `paho-mqtt`
- `python-rtmidi`

### Setup Instructions

1. **pip** :

- On Debian-based systems:

```sh
sudo apt update
sudo apt install python3-pip -y
```

- On Red Hat-based systems:

```sh
sudo yum install python3-pip -y
```

- On macOS:

```sh
brew install python
```

2. **Clone the Repository** :

```sh
git clone <your-repo-url>
cd <your-repo-directory>
```

3. **Install Dependencies** :

```sh
pip3 install paho-mqtt python-rtmidi
```

4. **Run the Script** :

```sh
python3 midi2broker.py --host localhost --port 1883 --midiport 1 --topicprefix midi
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
