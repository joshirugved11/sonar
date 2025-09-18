import platform, os, re, webbrowser, subprocess
from typing import Tuple

OS = platform.system().lower()

def open_url(url: str):
    webbrowser.open(url)

def open_app_windows(app_name: str):
    # 'start' is shell built-in
    os.system(f'start "" "{app_name}"')

def open_app_mac(app_name: str):
    subprocess.run(["open", "-a", app_name])

def open_app_linux(app_name: str):
    # try desktop-open or direct command
    try:
        subprocess.run([app_name], check=False)
    except Exception:
        subprocess.run(["xdg-open", app_name], check=False)

def open_application(app_name: str):
    """Try to open an application by name. app_name can be 'chrome' or 'WhatsApp'."""
    app_name = app_name.strip()
    if re.search(r"https?://", app_name):
        open_url(app_name)
        return True
    if OS.startswith("windows"):
        open_app_windows(app_name)
        return True
    elif OS.startswith("darwin"):
        open_app_mac(app_name)
        return True
    else:
        open_app_linux(app_name)
        return True

def call_number_or_contact(contact: str):
    contact = contact.strip()
    # if phone digits:
    if re.fullmatch(r"[\d\+\- ]+", contact):
        tel = f"tel:{contact}"
        webbrowser.open(tel)
        return True
    # if likely contact name: try opening Skype search or Zoom not available generically
    return False

def perform_action_from_intent(action: str, target: str, extra: dict = None) -> Tuple[bool, str]:
    try:
        if action == "open_app":
            open_application(target)
            return True, f"Opening {target}"
        if action == "open_url":
            open_url(target)
            return True, f"Opening URL {target}"
        if action == "call":
            ok = call_number_or_contact(target)
            return ok, "Calling..." if ok else "Could not place call"
        return False, "No action"
    except Exception as e:
        return False, f"Action error: {e}"
