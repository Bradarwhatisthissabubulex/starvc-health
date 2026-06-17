# StarVC Health Dashboard

A live health monitoring dashboard for StarVC services — API, Database, Socket, and Voice. Built with Flask and a clay-inspired UI with dark/light theme support.

## Features

- Real-time service health monitoring (auto-refresh every 10s)
- Per-service uptime percentage and status indicators
- Active socket connection count
- Memory usage display
- Dark/light theme toggle (persisted in localStorage)
- Responsive design

## Usage

```bash
pip install flask
python starvc_dashboard.py
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API 

The dashboard exposes a `/api/health` endpoint that proxies data from [starvc.ir/api/health](https://starvc.ir/api/health).

## License

MIT — see [LICENSE](LICENSE.md) for details.
