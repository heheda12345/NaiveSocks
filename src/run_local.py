import argparse
import sys

from core.password import InvalidPasswordError, loadsPassword
from core.local import LocalServer
from utils import config as lsConfig
from utils.utils import NetAddr

def run_local(config: lsConfig.Config):
    local = LocalServer(config.password,
                        NetAddr(config.localAddr,config.localPort),
                        NetAddr(config.serverAddr, config.serverPort))
    local.start()


def main():
    parser = argparse.ArgumentParser(
        description='A naive tunnel proxy that helps you bypass firewalls')
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
        '-u',
        metavar='URL',
        help='url contains server address, port and password')
    proxy_options.add_argument(
        '-s', metavar='SERVER_ADDR', help='server address')
    proxy_options.add_argument(
        '-p',
        metavar='SERVER_PORT',
        type=int,
        help='server port, default: 8388')
    proxy_options.add_argument(
        '-b',
        metavar='LOCAL_ADDR',
        help='local binding address, default: 127.0.0.1')
    proxy_options.add_argument(
        '-l', metavar='LOCAL_PORT', type=int, help='local port, default: 2333')
    proxy_options.add_argument('-k', metavar='PASSWORD', help='password')

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

    if args.u:
        try:
            url_config = lsConfig.loadURL(args.u)
        except lsConfig.InvalidURLError:
            parser.print_usage()
            print(f'invalid config URL {args.u!r}')
            sys.exit(1)
        config = config._replace(**url_config._asdict())

    if args.s:
        serverAddr = args.s
        config = config._replace(serverAddr=serverAddr)

    if args.p:
        serverPort = args.p
        config = config._replace(serverPort=serverPort)

    if args.b:
        localAddr = args.b
        config = config._replace(localAddr=localAddr)

    if args.l:
        localPort = args.l
        config = config._replace(localPort=localPort)

    if args.k:
        try:
            password = args.k
            config = config._replace(password=password)
        except InvalidPasswordError:
            parser.print_usage()
            print('invalid password')
            sys.exit(1)

    if config.localAddr is None:
        config = config._replace(localAddr='127.0.0.1')

    if config.localPort is None:
        config = config._replace(localPort=2333)

    if config.serverPort is None:
        config = config._replace(serverPort=8388)

    if config.password is None:
        parser.print_usage()
        print('need PASSWORD, please use [-k PASSWORD]')
        sys.exit(1)

    if config.serverAddr is None:
        parser.print_usage()
        print('need SERVER_ADDR, please use [-s SERVER_ADDR]')

    if args.save:
        print(f'dump config file into {args.save!r}')
        with open(args.save, 'w', encoding='utf-8') as f:
            lsConfig.dump(f, config)

    run_local(config)


if __name__ == '__main__':
    main()
