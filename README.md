# frame



A Raspberry Pi app for the [Pimoroni Inky Impression 7.3"](https://shop.pimoroni.com/products/inky-impression-7-3) 7-colour e-ink display.

## Scripts

| Script | Description |
|---|---|
| `inky_app.py` | Displays a calendar view: upcoming Google Calendar events, current weather (OpenWeatherMap) and a random quote (ZenQuotes) |
| `guest_wifi.py` | Displays a guest WiFi screen: welcome text and a scannable QR code to join the network |
| `buttons.py` | Runs as a systemd service, monitors the 4 hardware buttons — button A shows the WiFi screen, button B shows the calendar |

## Configuration

Copy `config.txt.default` to `config.txt` and fill in the values:

```ini
[googlecalendar]
CALENDAR_ID=<google calendar id>

[openweathermap]
LAT=<latitude>
LON=<longitude>
API_KEY=<openweathermap-api-key>

[local]
LOCALE=en_GB
LANG=en

[wifi]
SSID=<network name>
PASSWORD=<password>
```

Google OAuth2 credentials (`credentials.json`, `token.json`) are required for calendar access — see the [Google Calendar API quickstart](https://developers.google.com/calendar/api/quickstart/python).

## Setup on the Pi

### 1. Create the virtualenv

Pimoroni has a GitHub repository with examples, it also contains an installer that will create a virtualenv with all the display dependencies, this is the easiest way to get the dependencies installed

```bash
git clone https://github.com/pimoroni/inky
cd inky
./install.sh
```

Accept all prompts. This creates `~/.virtualenvs/pimoroni/` and installs `inky`, `Pillow`, `numpy`, `gpiod`, `gpiodevice` and the font packages.

### 2. Install additional dependencies

```bash
source ~/.virtualenvs/pimoroni/bin/activate
pip install google-api-python-client google-auth-oauthlib qrcode
```

### 3. Install and start the button monitor service

```bash
sudo cp inky-buttons.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now inky-buttons
```


### 4. Cron job to update the calendar view

The scripts runs once, if you want uptodate calendar events, you need to run it reguraly
you can add a cron job to do so, his one will run it every hour, update the path to your situation.

```
*/60 * * * * <path_to_scripts>/run_cal.sh
```


## Troubleshooting

To see all logging for the scripts:

```bash
journalctl -u inky-buttons -f   # follow live logs
```

Restart the s
```
sudo systemctl restart inky-buttons
```
