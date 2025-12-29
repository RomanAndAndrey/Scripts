import argparse
import sys
import time


def main():
    parser = argparse.ArgumentParser(description="Test script for Script Launcher")
    parser.add_argument("--count", type=int, default=10, help="Number of iterations")
    parser.add_argument("--message", type=str, default="Probing", help="Message to print")

    args = parser.parse_args()

    print(f"Starting test script with count={args.count} and message='{args.message}'")
    sys.stdout.flush()

    for i in range(args.count):
        print(f"[{i+1}/{args.count}] {args.message}...")
        sys.stdout.flush()  # Важно для реального времени
        time.sleep(0.5)

    print("Test script completed successfully.")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
