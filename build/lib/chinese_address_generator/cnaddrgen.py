#!/usr/bin/env python3
import argparse
from chinese_address_generator import generator
import sys
import errno

version = '0.2.0'

def main():
    parser = argparse.ArgumentParser(description="Chinese address generator")

    parser.add_argument("--level", "-l", type=int,
                        choices=[1, 2, 3, 4], required=True, help="Level of address")

    parser.add_argument("--num", "-n", type=int,
                        required=True, help="Number of addresses to generate.")

    parser.add_argument("--version", "-v", action='version', version=f'chinese-address-generator v{version}',
                        help="Version of chinese-address-generator")

    args = parser.parse_args()

    if args.num <= 0:
        print("Error: num must > 0", file=sys.stderr)
        return errno.EINVAL

    for _ in range(args.num):
        if args.level == 1:
            print(generator.generatelevel1())
        elif args.level == 2:
            print(generator.generatelevel2())
        elif args.level == 3:
            print(generator.generatelevel3())
        else:
            print(generator.generatelevel4())
    
    return 0

if __name__ == "__main__":
    main()