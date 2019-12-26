import circleci, github
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--project')
    parser.add_argument('--token')
    args = parser.parse_args()
