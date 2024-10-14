import argparse

import uvicorn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="Port", default=8000)
    parser.add_argument("--host", help="Host", default="127.0.0.1")

    args = parser.parse_args()

    uvicorn.run("route:app", host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    main()