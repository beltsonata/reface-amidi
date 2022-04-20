from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
import commands
import util


MIN_TIMEOUT = 2


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-t', '--timeout', help="Timeout on idle in seconds", 
                        type=int, default=2)
    parser.add_argument('-s', '--skip-prompt', 
                        help="Don't prompt if the file already exists",
                        action="store_true", default=False)
    parser.add_argument('filepath')
    
    args = parser.parse_args()
    
    if args.timeout < MIN_TIMEOUT:
        raise ArgumentTypeError(f"Bad timeout value, must be >= {MIN_TIMEOUT}")
    
    return args


if __name__ == '__main__':
    args = get_args()
    device = util.get_reface()
    
    path = Path(args.filepath).resolve()

    if path.is_dir():
        print('Path specified is a directory.')
        exit(1)
    elif path.is_file() and not args.skip_prompt:
        util.prompt_overwrite(path)
    
    commands.capture_patch(device, args.filepath, str(args.timeout))

    
    
    