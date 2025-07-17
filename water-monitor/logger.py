import logging
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Avoid adding multiple handlers if re-imported
if not logger.handlers:
    rich_handler = RichHandler(rich_tracebacks=True, markup=True, show_time=True, show_path=False)
    formatter = logging.Formatter("%(message)s")

    rich_handler.setFormatter(formatter)
    logger.addHandler(rich_handler)