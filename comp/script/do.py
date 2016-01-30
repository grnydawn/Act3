# do.py
import os

def build(cmd):
    os.system('cd /home/work; %s'%cmd)

def run(cmd):
    os.system('cd /home/work; %s'%cmd)

def ref_timing(args):
    # preprocess commands


    # build commands
    if hasattr(args, 'build_cmd'):
        build(args.build_cmd)

    # run commands
    if hasattr(args, 'run_cmd'):
        run(args.run_cmd)

    # postprocess commands

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run computing order')
    parser.add_argument('command', metavar='command', type=str, help='do command.')
    parser.add_argument('--build_cmd', dest='build_cmd', action='store', nargs='?', help='Specify build commands.')
    parser.add_argument('--run_cmd', dest='run_cmd', action='store', nargs='?', help='Specify run commands.')

    args = parser.parse_args()

    if args.command=='ref_timing':
        ref_timing(args)
    else:
        print('Unknown do command')

if __name__=='__main__':
    main()
