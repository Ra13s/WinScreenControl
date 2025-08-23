#!/usr/bin/env python3
"""
Simple Monitor Control Script
Controls monitor brightness and contrast via DDC/CI.

Examples:
  python monitor_control.py list
  python monitor_control.py get [monitor]
  python monitor_control.py brightness 75 [monitor]
  python monitor_control.py contrast 40 [monitor]
  python monitor_control.py preset reading [monitor]
  python monitor_control.py adjust-brightness -10 [monitor]
  python monitor_control.py adjust-contrast 5 [monitor]

Where [monitor] is an optional zero-based monitor index (default 0).
"""

import sys
import argparse
from monitorcontrol import get_monitors, Monitor  # noqa: F401 (Monitor used via context manager)
from typing import Optional


def clamp(value: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, value))


def int_0_100(s: str) -> int:
    try:
        v = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError("must be an integer")
    if not (0 <= v <= 100):
        raise argparse.ArgumentTypeError("must be between 0 and 100")
    return v


class MonitorController:
    def __init__(self):
        self.monitors = []
        self.load_monitors()

    def load_monitors(self):
        """Detect and load available monitors"""
        try:
            self.monitors = get_monitors()
            print(f"Found {len(self.monitors)} monitor(s)")
            for i, monitor in enumerate(self.monitors):
                print(f"  Monitor {i}: {monitor}")
        except Exception as e:
            print(f"Error detecting monitors: {e}")
            sys.exit(1)

    def _validate_monitor_index(self, monitor_index: int) -> bool:
        """Validate monitor index"""
        if not self.monitors:
            print("No monitors detected")
            return False

        if monitor_index < 0 or monitor_index >= len(self.monitors):
            print(f"Invalid monitor index {monitor_index}. Available: 0-{len(self.monitors) - 1}")
            return False

        return True

    def list_monitors(self):
        """List all detected monitors and their current settings"""
        print(f"\nDetected {len(self.monitors)} monitor(s):")
        for i, monitor in enumerate(self.monitors):
            print(f"  [{i}] {monitor}")
            try:
                with monitor:
                    brightness = monitor.get_luminance()
                    contrast = monitor.get_contrast()
                    print(f"      Brightness: {brightness}%, Contrast: {contrast}%")
            except Exception as e:
                print(f"      Error reading settings: {e}")

    def set_brightness(self, monitor_index: int = 0, brightness: int = 50) -> bool:
        """Set brightness for specified monitor (0-100)"""
        if not self._validate_monitor_index(monitor_index):
            return False

        brightness = clamp(brightness, 0, 100)

        try:
            with self.monitors[monitor_index] as monitor:
                monitor.set_luminance(brightness)
                print(f"Set monitor {monitor_index} brightness to {brightness}%")
                return True
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False

    def set_contrast(self, monitor_index: int = 0, contrast: int = 50) -> bool:
        """Set contrast for specified monitor (0-100)"""
        if not self._validate_monitor_index(monitor_index):
            return False

        contrast = clamp(contrast, 0, 100)

        try:
            with self.monitors[monitor_index] as monitor:
                monitor.set_contrast(contrast)
                print(f"Set monitor {monitor_index} contrast to {contrast}%")
                return True
        except Exception as e:
            print(f"Error setting contrast: {e}")
            return False

    def get_brightness(self, monitor_index: int = 0) -> Optional[int]:
        """Get current brightness for specified monitor"""
        if not self._validate_monitor_index(monitor_index):
            return None

        try:
            with self.monitors[monitor_index] as monitor:
                brightness = monitor.get_luminance()
                print(f"Monitor {monitor_index} brightness: {brightness}%")
                return brightness
        except Exception as e:
            print(f"Error getting brightness: {e}")
            return None

    def get_contrast(self, monitor_index: int = 0) -> Optional[int]:
        """Get current contrast for specified monitor"""
        if not self._validate_monitor_index(monitor_index):
            return None

        try:
            with self.monitors[monitor_index] as monitor:
                contrast = monitor.get_contrast()
                print(f"Monitor {monitor_index} contrast: {contrast}%")
                return contrast
        except Exception as e:
            print(f"Error getting contrast: {e}")
            return None

    def adjust_brightness(self, monitor_index: int = 0, delta: int = 10) -> bool:
        """Adjust brightness by delta amount"""
        current = self.get_brightness(monitor_index)
        if current is None:
            return False
        return self.set_brightness(monitor_index, current + delta)

    def adjust_contrast(self, monitor_index: int = 0, delta: int = 10) -> bool:
        """Adjust contrast by delta amount"""
        current = self.get_contrast(monitor_index)
        if current is None:
            return False
        return self.set_contrast(monitor_index, current + delta)

    def set_preset(self, monitor_index: int = 0, preset_name: str = "normal") -> bool:
        """Apply predefined presets"""
        presets = {
            "bright": {"brightness": 90, "contrast": 75},
            "normal": {"brightness": 50, "contrast": 50},
            "dim": {"brightness": 20, "contrast": 40},
            "night": {"brightness": 15, "contrast": 30},
            "gaming": {"brightness": 70, "contrast": 80},
            "reading": {"brightness": 40, "contrast": 60},
            "set-30": {"brightness": 30, "contrast": 30},
            "set-40": {"brightness": 40, "contrast": 40},
            "set-75": {"brightness": 75, "contrast": 75},
        }

        if preset_name not in presets:
            print(f"Unknown preset '{preset_name}'. Available: {', '.join(presets.keys())}")
            return False

        preset = presets[preset_name]
        ok1 = self.set_brightness(monitor_index, preset["brightness"])
        ok2 = self.set_contrast(monitor_index, preset["contrast"])
        if ok1 and ok2:
            print(f"Applied '{preset_name}' preset to monitor {monitor_index}")
            return True
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="monitor_control.py",
        description="Control monitor brightness and contrast via DDC/CI",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List monitors and current settings")

    p_get = sub.add_parser("get", help="Get current brightness and contrast")
    p_get.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    p_bri = sub.add_parser("brightness", help="Set brightness (0-100)")
    p_bri.add_argument("value", type=int_0_100, help="Brightness percentage 0-100")
    p_bri.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    p_con = sub.add_parser("contrast", help="Set contrast (0-100)")
    p_con.add_argument("value", type=int_0_100, help="Contrast percentage 0-100")
    p_con.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    p_pre = sub.add_parser("preset", help="Apply a preset")
    p_pre.add_argument(
        "name",
        choices=["bright", "normal", "dim", "night", "gaming", "reading", "set-30", "set-40", "set-75"],
        help="Preset name",
    )
    p_pre.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    p_ab = sub.add_parser("adjust-brightness", help="Adjust brightness by ±delta")
    p_ab.add_argument("delta", type=int, help="Signed delta, e.g., +10 or -5")
    p_ab.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    p_ac = sub.add_parser("adjust-contrast", help="Adjust contrast by ±delta")
    p_ac.add_argument("delta", type=int, help="Signed delta, e.g., +10 or -5")
    p_ac.add_argument("monitor", type=int, nargs="?", default=0, help="Monitor index (default 0)")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    controller = MonitorController()

    if args.cmd == "list":
        controller.list_monitors()

    elif args.cmd == "get":
        controller.get_brightness(args.monitor)
        controller.get_contrast(args.monitor)

    elif args.cmd == "brightness":
        controller.set_brightness(args.monitor, args.value)

    elif args.cmd == "contrast":
        controller.set_contrast(args.monitor, args.value)

    elif args.cmd == "preset":
        controller.set_preset(args.monitor, args.name)

    elif args.cmd == "adjust-brightness":
        controller.adjust_brightness(args.monitor, args.delta)

    elif args.cmd == "adjust-contrast":
        controller.adjust_contrast(args.monitor, args.delta)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
