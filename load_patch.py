from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import util
import commands


def get_args():
    parser = ArgumentParser()
    parser.add_argument('filepath')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    device = util.get_reface()
    path = Path(args.filepath).resolve()
    
    if path.is_dir():
        print('Path specified is a directory.')
        exit(1)
    elif not path.is_file():
        print(f'File not found at "{path}"')
    
    print(f'Sending patch "{args.filepath}" to device at port ' 
          f'"{device[1]}" ({device[0]})')
    
    commands.send_patch(device, str(path))
        