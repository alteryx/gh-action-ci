import circleci, github
import subprocess
from argparse import ArgumentParser

if __name__ == '__main__':
    command = ArgumentParser()
    command.add_argument('--x0')

    args = command.parse_args()
    subprocess.run(["echo", "x0: %s" % args.x0])
    subprocess.run(["echo", "::set-output name=y0::%s" % args.x0])