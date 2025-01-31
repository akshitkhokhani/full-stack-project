import uvicorn
import os
from app.main import create_application

app = create_application()

"""
This main file and we have to run this file and this application
runs on uvicorn server on 8000 port.
"""

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if __name__ == "__main__":
    if DEBUG == True:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
            lifespan="on",
            workers=1,
            proxy_headers=True,
            reload=bool(DEBUG),
            ws_ping_interval=600,
            ws_ping_timeout=600,
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8088,
            lifespan="on",
            workers=1,
            proxy_headers=True,
            reload=bool(DEBUG),
            ws_ping_interval=600,
            ws_ping_timeout=600,
        )
