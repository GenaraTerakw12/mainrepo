import logging
from datetime import datetime 
import time 
import sys
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler(sys.stdout)])

while True:
    logging.info(f"Currently waiting for job : {datetime.now()}")
    time.sleep(10)

