import argparse
import sys

from Crypto.Hash import SHA256
import base64

from utils import config as cfg
from core.password import InvalidPasswordError, loadPassword, dumpPassword, randomPassword
from core.remote import RemoteServer
from utils.utils import NetAddr

def run_remote(config: cfg.Config):
    remote = RemoteServer(config.key,
                          NetAddr(config.serverAddr, config.serverPort))
    remote.start()

def main():
    parser = argparse.ArgumentParser(
        description='A naive tunnel proxy that helps you protect your connections')
    parser.add_argument(
        '--version', action='store_true', default=False, help='show version information')
    
    proxy_options = parser.add_argument_group('Proxy options')

    proxy_options.add_argument(
        '--save', metavar='CONFIG', help='path to dump config')
    proxy_options.add_argument(
        '-c', metavar='CONFIG', help='path to config file')
    proxy_options.add_argument(
        '-e', metavar='KEY', help='path to key')
    proxy_options.add_argument(
        '-k', metavar='PASSWORD', help='password')
    proxy_options.add_argument(
        '-s', metavar='SERVER_ADDR', help='server address')
    proxy_options.add_argument(
        '-p', metavar='SERVER_PORT', type=int, help='server port, default: 8388')
    proxy_options.add_argument(
        '--random', action='store_true', default=False, help='generate a random key to use')

    args = parser.parse_args()

    if args.version:
        print('naivesocks 0.1.0')
        sys.exit(0)
    
    config = cfg.Config(None, None, None, None, None, None)

    if args.c:
        try:
            with open(args.c, encoding='utf-8') as f:
                file_config = cfg.load(f)
        except cfg.InvalidFileError:
            parser.print_usage()
            print(f'invalid config file {args.c!r}')
            sys.exit(1)
        except FileNotFoundError:
            parser.print_usage()
            print(f'config file {args.c!r} not found')
            sys.exit(1)
        config = config._replace(**file_config._asdict())

    if args.e:
        key = args.e
        config = config._replace(key=key)

    if args.k:
        if config.key:
            parser.print_usage()
            print('use both PASSWORD and PRIVATE_KEY is not allowed')
            sys.exit(1)
        password = args.k
        config = config._replace(password=password)

    if args.s:
        serverAddr = args.s
        config = config._replace(serverAddr=serverAddr)

    if args.p:
        serverPort = args.p
        config = config._replace(serverPort=serverPort)

    if config.serverAddr is None:
        config = config._replace(serverAddr='0.0.0.0')

    if config.serverPort is None:
        config = config._replace(serverPort=8388)

    if config.key:
        try:
            with open(config.key,'r') as f:
                key = loadPassword(f.read())
        except ValueError:
            parser.print_usage()
            print(f'invalid private key {config.key!r}')
            sys.exit(1)
        except FileNotFoundError:
            parser.print_usage()
            print(f'config file {config.key!r} not found')
            sys.exit(1)
    elif config.password:
        h = SHA256.new()
        h.update(config.password.encode('utf-8'))
        key = h.digest()
    elif args.random:
        print('generate random password')
        key = randomPassword()
        with open('key.pem', 'wb') as f:
            f.write(dumpPassword(key))
        config = config._replace(key='key.pem')
    else:
        parser.print_usage()
        print('need PASSWORD or PRIVATE_KEY, please use [-k PASSWORD] [-e PRIVATE_KEY] or '
              'use [--random] to generate a random password')
        sys.exit(1)

    if args.save:
        print(f'dump config file into {args.save!r}')
        with open(args.save, 'w', encoding='utf-8') as f:
            cfg.dump(f, config)

    config = config._replace(key=key)

    run_remote(config)


if __name__ == '__main__':
    main()
