#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Improved wallpaper shuffle script for macOS.

Author: Jannik Schmied, 2024
"""
import argparse
import filetype
import matplotlib.pyplot as plt
import os
import random
import subprocess
import sys
import time

from appscript import app, mactypes
from collections import defaultdict


class Wallpaper:
    def __init__(self, path, analysis=False, restore=False):
        self.path = path
        self.analysis = analysis
        self.restore = restore
        self.images = [image for image in [file for file in os.listdir(self.path) if not os.path.isdir(os.path.join(self.path, file))] if filetype.is_image(os.path.join(self.path, image))]
        self.current_wallpaper = app('Finder').desktop_picture.get()

        if self.restore:
            print("[*] Saved initial wallpaper (-r specified)")
            self.initial_wallpaper = self.current_wallpaper

        self.total_wallpapers = len(self.images)

        if self.total_wallpapers == 0:
            notify("WallpaperShuffle", "Error: No images found in specified directory!")
            raise ValueError("[!] No images found in specified directory!")

        self.total_wallpapers_shuffled = 0
        self.last_img_name_buf = 0

        if self.analysis:
            self.image_counts = defaultdict(int)

    def next(self):
        # Get random image from folder
        self.current_wallpaper = random.choice(self.images)

        # Set wallpaper
        app('Finder').desktop_picture.set(mactypes.File(os.path.join(self.path, self.current_wallpaper)))
        print(f"[i] Current wallpaper: {self.current_wallpaper.ljust(self.last_img_name_buf)}", end="\r", flush=True)

        # Increment wallpaper counter and sleep for interval
        self.last_img_name_buf = len(self.current_wallpaper)
        self.total_wallpapers_shuffled += 1

        if self.analysis:
            self.image_counts[self.current_wallpaper] += 1

    def update(self):
        self.images = [image for image in [file for file in os.listdir(self.path) if not os.path.isdir(os.path.join(self.path, file))] if filetype.is_image(os.path.join(self.path, image))]
        if self.total_wallpapers != len(self.images):
            print(f"[*] Updated images (Total: {self.total_wallpapers} -> {len(self.images)})")
            notify("WallpaperShuffle", f"Updated images (Total: {self.total_wallpapers} -> {len(self.images)})")
            self.total_wallpapers = len(self.images)

    def analyze(self):
        mean_usage = sum(self.image_counts.values()) / len(self.image_counts)
        std_deviation = (sum((x - mean_usage) ** 2 for x in self.image_counts.values()) / len(self.image_counts)) ** 0.5

        print(f"[i] Mean Usage: {mean_usage}")
        print(f"[i] Standard Deviation: {std_deviation}")

        plt.bar(self.image_counts.keys(), self.image_counts.values())
        plt.xlabel("Images")
        plt.ylabel("Usage Count")
        plt.title("Histogram of Image Usage")
        plt.xticks(rotation=90)
        plt.show()

    def restore_wallpaper(self):
        app('Finder').desktop_picture.set(self.initial_wallpaper)
        print("[*] Restored initial wallpaper")

    @property
    def wallpaper_counter(self):
        return self.total_wallpapers_shuffled


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
    parser.add_argument("--analyze", "-a", help="Analyze image usage", action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isdir(args.path):
        notify("WallpaperShuffle", "Error: Path does not exist or is not a directory!")
        raise ValueError("[!] Path does not exist or is not a directory!")

    wallpaper = Wallpaper(args.path, analysis=args.analyze, restore=args.restore)

    print("[*] Starting wallpaper shuffle. Press CTRL+C to stop.")
    notify("WallpaperShuffle", "Starting wallpaper shuffle. Press CTRL+C to stop.")

    while True:
        try:
            wallpaper.next()
            wallpaper.update()
            time.sleep(args.interval)

        except KeyboardInterrupt:
            print(f"\n[*] Stopped. Shuffled {wallpaper.wallpaper_counter} wallpapers.")
            break

        except Exception as e:
            notify("WallpaperShuffle", f"Error: {e}")
            continue

    if args.restore:
        wallpaper.restore_wallpaper()

    if args.analyze:
        wallpaper.analyze()

    print("[*] Done. Exiting.")
    sys.exit(0)


if __name__ == "__main__":
    main()
