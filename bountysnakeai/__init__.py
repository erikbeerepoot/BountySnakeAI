import logging
import sys

log = logging.getLogger(__name__)
log_level = logging.DEBUG
log.setLevel(log_level)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(log_level)
formatter = logging.Formatter('%(asctime)s - %(name)-20s - %(levelname)7s - %(message)s')
stdout_handler.setFormatter(formatter)
log.addHandler(stdout_handler)
