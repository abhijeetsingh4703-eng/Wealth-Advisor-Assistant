import logging
import json
from datetime import datetime
from logging.handlers import RotatingFileHandler

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName
        }
        if hasattr(record, "session_id"):
             log_record["session_id"] = record.session_id
        return json.dumps(log_record)

def setup_logger():
    logger = logging.getLogger("wealth_advisor")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    fh = RotatingFileHandler("agent_execution.log", maxBytes=10485760, backupCount=5)
    fh.setLevel(logging.INFO)
    json_formatter = JsonFormatter()
    fh.setFormatter(json_formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

logger = setup_logger()
