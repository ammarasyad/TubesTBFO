import sys
import parser


def main():
    argc = len(sys.argv)
    if argc != 2:
        print("Usage: python main.py <filename>.js")
        exit(1)
    # harusnya pake argparse cuman gpp dah
    parser.parse(sys.argv[1])


if __name__ == "__main__":
    main()
