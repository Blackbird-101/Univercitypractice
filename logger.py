import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #level=logging.ERROR,
    level=logging.INFO,
    filename='job_link.log'
)
logger = logging.getLogger(__name__)