import argparse

import uvicorn

from core.config import config


def main():
    HOST = config.HOST
    PORT = config.PORT

    parser = argparse.ArgumentParser(
        description="Run the server with specified host and port."
    )
    parser.add_argument(
        "--host", type=str, default=HOST, help=f"Host address (default: {HOST})"
    )
    parser.add_argument(
        "--port", type=int, default=PORT, help=f"Port number (default: {PORT})"
    )

    args = parser.parse_args()

    run_server(args.host, args.port)


def run_server(host: str, port: int) -> None:
    uvicorn.run("core:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
