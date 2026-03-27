# import logging

# logging.basicConfig(
#     filename="logs/app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
import logging
import os

# -------------------------------
# CREATE LOGS DIRECTORY (IMPORTANT)
# -------------------------------
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# -------------------------------
# CONFIGURE LOGGING
# -------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# CREATE LOGGER INSTANCE
# -------------------------------
logger = logging.getLogger(__name__)

# -------------------------------
# TEST LOG (VERY IMPORTANT)
# -------------------------------
logger.info("🔥 Logger initialized")