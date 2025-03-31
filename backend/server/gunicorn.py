from gunicorn.app.base import BaseApplication

def create_options(
    host: str = "0.0.0.0",
    port: int = 8000,
    workers: int = 1,
    forwarded_allow_ips: str = None,
    keepalive: int = None,
):
    return {
        "accesslog": "-",
        "errorlog": "-",
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "forwarded_allow_ips": forwarded_allow_ips or "*",
        "keepalive": keepalive or 120,
    }

class GunicornServer(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    @property
    def config_options(self) -> dict:
        return {
            k: v 
            for k, v in self.options.items()
            if k in self.cfg.settings and v is not None
        }

    def load_config(self) -> None:
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application