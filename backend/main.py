import sys
import pytest
import subprocess
import time

from app.application import app
from app.config.settings import settings

from server.gunicorn import GunicornServer, create_options

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['test', 'production']:
        print("Usage: python main.py [test|production]")
        sys.exit(1)
    option = sys.argv[1]
    
    output = subprocess.check_output(["alembic", "upgrade", "head"], text=True)
    print(output)
 
    if option == 'test':
        pytest.main(['-s', '-v'])
    elif option == 'production':
        server = GunicornServer(
            app=app, 
            options=create_options(
                host=settings.HOST,
                port=settings.PORT,
                workers=settings.WORKERS,
                forwarded_allow_ips=settings.FORWARDED_ALLOW_IPS,
                keepalive=settings.KEEPALIVE
            )
        )
        server.run()

if __name__ == '__main__':
    main()
