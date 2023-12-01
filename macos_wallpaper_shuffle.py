#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Improved wallpaper shuffle script for macOS.

Author: Jannik Schmied, 2023
"""
import argparse
import filetype
import os
import random
import subprocess
import sys
import time

from appscript import app, mactypes


def notify(title: str, text: str, icon_path: str = "./assets/macos_beta.icns"):
    subprocess.run([
        "terminal-notifier",
        "-title", title,
        "-message", text,
        "-appIcon", icon_path
    ], check=True)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", "-p", help="Path to folder containing images", type=str, required=True)
    parser.add_argument("--interval", "-i", help="Interval in seconds between wallpaper changes", type=int, required=True, default=60)
    parser.add_argument("--restore", "-r", help="Restore previous wallpaper on exit", action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isdir(args.path):
        notify("WallpaperShuffle", "Error: Path does not exist or is not a directory!")
        raise ValueError("[!] Path does not exist or is not a directory!")

    if args.restore:
        # Get current wallpaper
        print("[*] Saving current wallpaper")
        current_wallpaper = app('Finder').desktop_picture.get()

    images: list = [image for image in [file for file in os.listdir(args.path) if not os.path.isdir(os.path.join(args.path, file))] if filetype.is_image(os.path.join(args.path, image))]

    if len(images) == 0:
        notify("WallpaperShuffle", "Error: No images found in specified directory!")
        raise ValueError("[!] No images found in specified directory!")

    wallpaper_counter: int = 0

    print("[*] Starting wallpaper shuffle. Press CTRL+C to stop.")
    notify("WallpaperShuffle", "Starting wallpaper shuffle. Press CTRL+C to stop.")

    while True:
        try:
            # Get random image from folder
            image = random.choice(images)

            # Set wallpaper
            app('Finder').desktop_picture.set(mactypes.File(os.path.join(args.path, image)))

            # Increment wallpaper counter and sleep for interval
            wallpaper_counter += 1
            time.sleep(args.interval)

        except KeyboardInterrupt:
            print(f"\n[i] Stopped. Shuffled {wallpaper_counter} wallpapers.")
            break

        except Exception as e:
            notify("WallpaperShuffle", f"Error: {e}")
            continue

    if args.restore:
        # Reset wallpaper
        print("[*] Restoring initial wallpaper")
        app('Finder').desktop_picture.set(current_wallpaper)

    print("[*] Done. Exiting.")
    sys.exit(0)


if __name__ == "__main__":
    main()
