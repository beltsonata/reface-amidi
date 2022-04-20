import subprocess
import logging
import threading
import time

from save_patch import MIN_TIMEOUT

log = logging.getLogger(__name__)

AMIDI_LIST_DEVICES='amidi -l'

REFACE_BULK_REQUEST = {
    'CS': 'F0 43 20 7F 1C 03 0E 0F 00 F7',
    'CP': 'F0 43 20 7F 1C 04 0E 0F 00 F7',
    'DX': 'F0 43 20 7F 1C 05 0E 0F 00 F7',
    'YC': 'F0 43 20 7F 1C 06 0E 0F 00 F7',
}

def run(command):
    """
    Run a sub process, check it returned 0 and return the stdout
    """
    raw_out = subprocess.run(command, shell=True, check=True, capture_output=True)
    out = raw_out.stdout.decode('utf-8').strip()
    log.debug(f"({command}): out: {out}")
    return out


def send_cmd(device, args):
    """Send an amidi command to the device"""
    command = [
        'amidi',
        '-p',
        device[1],
    ] + args
    return run(" ".join(command))


def send_hex(device, hex):
    """Send sysex hex to a device using amidi"""
    command = [
        '-S',
        hex,
    ]
    return send_cmd(device, command)


def send_bulk_request(device):
    print(device)
    reface_type = device[0].split(" ")[1]
    bulk_req = REFACE_BULK_REQUEST[reface_type]
    return send_hex(device, bulk_req)


def hex_listener(device, path, timeout):
    """
    Listens for hex coming from the Reface device
    and dumps it a file. Stops after <timeout> seconds
    have elapsed after no data has been received.

    Intended to be run in a separate thread to capture
    the output of dump requests until its killed.
    """
    command = [
        '--timeout',
        timeout,
        '--receive', 
        path,
    ]
    send_cmd(device, command)
    

def capture_patch(device, path, timeout):
    """Send a bulk request to the device and save the 
    response to a file."""
    print("Sending BULK REQUEST to device", device)
    t = threading.Thread(daemon=True, 
                         target=hex_listener, 
                         args=(device, path, timeout))
    t.start()
    # Wait for command in thread to start. Value must be less than <timeout>!
    time.sleep(1)

    send_bulk_request(device)
    print(f"Saving '{path}'")
    

def send_patch(device, path):
    """Send a patch from a sysex file to the reface"""
    send_cmd(device, ['--send', path])


def get_devices():
    """Return all connected devices (using amidi)"""
    out = run(AMIDI_LIST_DEVICES)
    lines = out.split('\n')
    if len(lines) < 2:
        return []
    
    devs_raw = lines[1:]
    devs = {}

    for n, device in enumerate(devs_raw, start=1):
        tokens = device.split()[1:]
        port = tokens[0]
        name = " ".join(tokens[1:])
        if 'reface' in name.lower():
            devs[str(n)] = (name, port)

    return devs

