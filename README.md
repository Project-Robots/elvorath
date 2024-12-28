# elvorath

A FastAPI Certificate Authority for the Orbit server.

## Installation

```bash
pip install elvorath
```

## Usage

```bash
uvicorn elvorath.main:app --workers 4 --port 5401 --host 0.0.0.0 --ssl-keyfile /path/to/keyfile.key --ssl-certfile /path/to/certfile.crt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT