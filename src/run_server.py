import argparse
import asyncio
import sys

from core.password import (InvalidPasswordError, dumpsPassword,
                                      loadsPassword, randomPassword)
from utils import config as lsConfig


def run_server(config: lsConfig.Config):
    print(config)


def main():
    parser = argparse.ArgumentParser(
        description='A light tunnel proxy that helps you bypass firewalls')
    parser.add_argument(
        '--version',
        action='store_true',
        default=False,
        help='show version information')

    proxy_options = parser.add_argument_group('Proxy options')

    proxy_options.add_argument(
        '--save', metavar='CONFIG', help='path to dump config')
    proxy_options.add_argument(
        '-c', metavar='CONFIG', help='path to config file')
    proxy_options.add_argument(
        '-s', metavar='SERVER_ADDR', help='server address, default: 0.0.0.0')
    proxy_options.add_argument(
        '-p',
        metavar='SERVER_PORT',
        type=int,
        help='server port, default: 8388')
    proxy_options.add_argument('-k', metavar='PASSWORD', help='password')
    proxy_options.add_argument(
        '--random',
        action='store_true',
        default=False,
        help='generate a random password to use')

    args = parser.parse_args()

    if args.version:
        print('lightsocks 0.1.0')
        sys.exit(0)

    config = lsConfig.Config(None, None, None, None, None)
    if args.c:
        try:
            with open(args.c, encoding='utf-8') as f:
                file_config = lsConfig.load(f)
        except lsConfig.InvalidFileError:
            parser.print_usage()
            print(f'invalid config file {args.c!r}')
            sys.exit(1)
        except FileNotFoundError:
            parser.print_usage()
            print(f'config file {args.c!r} not found')
            sys.exit(1)
        config = config._replace(**file_config._asdict())

    if args.s:
        serverAddr = args.s
        config = config._replace(serverAddr=serverAddr)

    if args.p:
        serverPort = args.p
        config = config._replace(serverPort=serverPort)

    if args.k:
        try:
            password = loadsPassword(args.k)
            config = config._replace(password=password)
        except InvalidPasswordError:
            parser.print_usage()
            print('invalid password')
            sys.exit(1)

    if config.serverAddr is None:
        config = config._replace(serverAddr='0.0.0.0')

    if config.serverPort is None:
        config = config._replace(serverPort=8388)

    if config.password is None and not args.random:
        parser.print_usage()
        print('need PASSWORD, please use [-k PASSWORD] or '
              'use [--random] to generate a random password')
        sys.exit(1)

    if args.random:
        print('generate random password')
        config = config._replace(password=randomPassword())

    if args.save:
        print(f'dump config file into {args.save!r}')
        with open(args.save, 'w', encoding='utf-8') as f:
            lsConfig.dump(f, config)

    run_server(config)


if __name__ == '__main__':
    main()
