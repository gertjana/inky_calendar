#!/usr/bin/env python3
import os
import configparser

from inky.auto import auto
from inky.inky_uc8159 import CLEAN
from PIL import Image, ImageDraw, ImageFont
from font_source_sans_pro import SourceSansProSemibold
import qrcode

welcome_font  = ImageFont.truetype(SourceSansProSemibold, 96)
subtitle_font = ImageFont.truetype(SourceSansProSemibold, 48)
label_font    = ImageFont.truetype(SourceSansProSemibold, 24)

def generateWifiQR(ssid, password):
    wifi_string = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(wifi_string)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_img = qr_img.resize((250, 250), Image.LANCZOS)
    return qr_img

def updateDisplay(ssid, password):
    disp = auto(ask_user=True, verbose=True)
    for _ in range(2):
        for y in range(disp.height - 1):
            for x in range(disp.width - 1):
                disp.set_pixel(x, y, CLEAN)

    img = Image.new("P", disp.resolution, disp.WHITE)
    canvas = ImageDraw.Draw(img)

    # Layout constants
    LEFT_COL_WIDTH  = disp.width * 2 // 3   # ~533px
    RIGHT_COL_START = LEFT_COL_WIDTH
    RIGHT_COL_WIDTH = disp.width - RIGHT_COL_START  # ~267px

    # Measure text
    welcome_bbox  = canvas.textbbox((0, 0), "Welkom",    font=welcome_font)
    subtitle_bbox = canvas.textbbox((0, 0), "bij Mo & Ted", font=subtitle_font)

    welcome_w  = welcome_bbox[2]  - welcome_bbox[0]
    welcome_h  = welcome_bbox[3]  - welcome_bbox[1]
    subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_h = subtitle_bbox[3] - subtitle_bbox[1]

    LINE_GAP    = 16
    block_h     = welcome_h + LINE_GAP + subtitle_h
    block_top   = (disp.height - block_h) // 2

    welcome_x  = (LEFT_COL_WIDTH - welcome_w)  // 2
    subtitle_x = (LEFT_COL_WIDTH - subtitle_w) // 2

    canvas.text((welcome_x,  block_top),                        "Welkom",     disp.BLACK, welcome_font)
    canvas.text((subtitle_x, block_top + welcome_h + LINE_GAP), "bij Mo & Ted", disp.BLACK, subtitle_font)

    # QR code block — "WiFi" label + QR + SSID, all centered in right third
    qr_img = generateWifiQR(ssid, password)

    wifi_label_bbox = canvas.textbbox((0, 0), "WiFi", font=label_font)
    ssid_bbox       = canvas.textbbox((0, 0), ssid,   font=label_font)
    wifi_label_w = wifi_label_bbox[2] - wifi_label_bbox[0]
    wifi_label_h = wifi_label_bbox[3] - wifi_label_bbox[1]
    ssid_w       = ssid_bbox[2]       - ssid_bbox[0]
    ssid_h       = ssid_bbox[3]       - ssid_bbox[1]

    QR_SIZE      = 250
    LABEL_GAP    = 8
    qr_block_h   = wifi_label_h + LABEL_GAP + QR_SIZE + LABEL_GAP + ssid_h
    qr_block_top = (disp.height - qr_block_h) // 2
    qr_center_x  = RIGHT_COL_START + RIGHT_COL_WIDTH // 2 - 64

    wifi_label_y = qr_block_top
    qr_y         = wifi_label_y + wifi_label_h + LABEL_GAP
    ssid_y       = qr_y + QR_SIZE + LABEL_GAP

    canvas.text((qr_center_x - wifi_label_w // 2, wifi_label_y), "WiFi", disp.BLACK, label_font)
    img.paste(qr_img, (qr_center_x - QR_SIZE // 2, qr_y))

    disp.set_image(img)
    disp.show()

def main():
    config = configparser.ConfigParser()
    try:
        config.read_file(open(os.getcwd() + '/config.txt'))
        ssid     = config.get('wifi', 'SSID',     raw=False)
        password = config.get('wifi', 'PASSWORD', raw=False)
    except Exception as e:
        print(f'Error getting config values: {e}')
        return

    updateDisplay(ssid, password)

if __name__ == "__main__":
    main()
