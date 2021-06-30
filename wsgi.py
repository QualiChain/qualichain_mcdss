import logging
import sys
from api.app import app
from MCDSS.settings import  API_PORT

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info("Starting Qualichain MCDSS")
    app.run(host='0.0.0.0', port=API_PORT, debug=True)

