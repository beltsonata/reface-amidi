import commands

def get_reface():
    device_choices = commands.get_devices()
    
    if not device_choices:
        print("No Reface CS found") 
        exit(1) 
    
    if len(device_choices) > 1:
        device = select_device(device_choices)
    else:
        device = list(device_choices.values()).pop()

    if not device:
        print('Aborting')
        exit(0)
    print('Using', device)

    return device


def select_device(devices):
    """Get the human to select a Reface, on the assumption
    that there might be more than one midi device connected"""
    print('Select device:\n')

    for num, (name, port) in devices.items():
        print(f' [{num}] Name: {name}, Port: {port}')
    
    print("\nEnter number to select device:")    
    choice = input("> ")    
    return devices.get(choice)


def prompt_overwrite(path):
    print(f'Overwrite file "{path}"?')
    if input("> ").lower() not in ["y", "yes"]:
        print("Aborting")
        exit(0)