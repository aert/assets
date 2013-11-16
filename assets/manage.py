#!/usr/bin/env python
import os
import sys


def main():
    setting_module = "assets.webui.settings.main"
    os.environ["DJANGO_SETTINGS_MODULE"] = setting_module

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
