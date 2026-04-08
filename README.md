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

```bash
# Install dependencies in the Pimoroni virtualenv
source ~/.virtualenvs/pimoroni/bin/activate
pip install qrcode

# Install and start the button monitor service
sudo cp inky-buttons.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now inky-buttons
```

## Useful commands

```bash
journalctl -u inky-buttons -f   # follow live logs
sudo systemctl restart inky-buttons
```
