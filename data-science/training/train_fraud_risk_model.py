"""Training entrypoint for the fraud/risk model. Reads features from feature-store."""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    print(f"training with config: {args.config}")


if __name__ == "__main__":
    main()
