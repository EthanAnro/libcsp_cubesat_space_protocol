#!/usr/bin/env python
# encoding: utf-8

import subprocess
import sys


def build_with_waf():
    target_os = 'posix'  # default OS
    options = sys.argv[1:]
    if (len(options) > 0) and not options[0].startswith('--'):
        target_os = options[0]
        options = options[1:]

    options += [
        '--with-os=' + target_os,
        '--enable-rdp',
        '--enable-promisc',
        '--enable-crc32',
        '--enable-hmac',
        '--enable-xtea',
        '--enable-dedup',
        '--with-loglevel=debug',
        '--enable-debug-timestamp'
    ]

    waf = ['./waf']
    if target_os in ['posix']:
        options += [
            '--enable-python3-bindings',
            '--enable-can-socketcan',
            '--with-driver-usart=linux',
            '--enable-if-zmqhub',
            '--enable-shlib'
        ]

    if target_os in ['macosx']:
        options += [
            '--with-driver-usart=linux',
        ]

    if target_os in ['windows']:
        options += [
            '--with-driver-usart=windows',
        ]
        waf = ['python', '-x', 'waf']

    # Build
    waf += ['distclean', 'configure', 'build']
    print("Waf build command:", waf)
    subprocess.check_call(waf + options +
                          ['--with-rtable=cidr', '--disable-stlib', '--disable-output'])
    subprocess.check_call(waf + options + ['--enable-examples'])


def main():
    build_with_waf()


if __name__ == '__main__':
    main()
