import subprocess
import time
import pexpect
import colorama

YUBIKEY_BIN = "/Applications/YubiKey\\ Manager.app/Contents/MacOS/ykman"

class TextStyle:
    # Text formatting
    BOLD = '\033[1m'
    RESET = '\033[0m'

    # Foreground colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'

# Logging
def LOG_INFO(string, start = "", end = ""):
    print(start + "[ LOG_INFO ]: " + string + TextStyle.RESET + end)

def LOG_ERROR(string, start = TextStyle.BOLD + TextStyle.RED, end = ""):
    print(start + "[ LOG_ERROR ]: " + string + TextStyle.RESET + end)

def LOG_RESULT(string, start = "", end = ""):
    print(start + "[ LOG_RESULT ]: " + string + TextStyle.RESET + end)

def check_yubikey_usb_status():
    command = YUBIKEY_BIN + " info | grep 'OTP' | grep -v ':'"
    LOG_INFO("Running Command: " + TextStyle.GREEN + command)
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=True).stdout.rstrip()

# Flip the switch
def run_ykman_usb_flip():
    try:
        enabled = False

        # Check YubiKey Current Status
        LOG_INFO("CHECK YUBIKEY CURRENT STATUS", TextStyle.BOLD + TextStyle.MAGENTA)
        result = check_yubikey_usb_status()
        LOG_INFO("YubiKey Info Output: " + TextStyle.GREEN + result, "", "\n")

        # Flip the Status
        LOG_INFO("FLIP THE STATUS", TextStyle.BOLD + TextStyle.MAGENTA)
        if "Enabled" in result:
            command = YUBIKEY_BIN + " config usb --disable OTP"
            LOG_INFO("DISABLING YUBIKEY", TextStyle.BOLD + TextStyle.RED)
        elif "Disabled" in result:
            command = YUBIKEY_BIN + " config usb --enable OTP"
            LOG_INFO("ENABLING YUBIKEY", TextStyle.BOLD + TextStyle.BLUE)
            enabled = True
        else:
            LOG_ERROR("OUTPUT NOT EXPECTED\n")
            exit()

        LOG_INFO("Running Command: " + TextStyle.GREEN + command, "", "\n")

        # Expect Script to interact with the bash
        child = pexpect.spawn(command)
        child.expect('Proceed?')
        child.sendline('Y')

        # Check New Status [ Also Verify? ]
        LOG_INFO("CHECK YUBIKEY NEW STATUS", TextStyle.BOLD + TextStyle.MAGENTA)
        result = check_yubikey_usb_status()
        LOG_INFO("New Status of YubiKey: " + TextStyle.GREEN + result, "", "\n")

        if enabled:
            LOG_RESULT("YUBIKEY ENABLED", TextStyle.BOLD + TextStyle.BLUE, "\n")
        else:
            LOG_RESULT("YUBIKEY DISABLED", TextStyle.BOLD + TextStyle.RED, "\n")

    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"Error: {e}")

run_ykman_usb_flip()
