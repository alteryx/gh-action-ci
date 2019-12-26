# import circleci, github
from argparse import ArgumentParser

if __name__ == '__main__':
    command = ArgumentParser()
    command.add_argument('--x0')

    args = command.parse_args()
    print('x0: %s' % args.x0)
    print('::set-output name=y0::%s' % args.x0)
