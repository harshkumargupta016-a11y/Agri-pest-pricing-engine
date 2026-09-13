import csv
import time
import logging
from typing import List
from .schemas import MandiPriceData
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def chunk_data(data: List[dict], chunk_size: int = 100):
    """Yield successive chunks from data to avoid memory overload."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def process_mandi_ingestion(filepath: str):
    start_time = time.time()
    valid_records = []
    errors = []
    
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Edge Case: Check for missing headers
            if not reader.fieldnames or "commodity" not in reader.fieldnames:
                raise ValueError("Corrupt file or missing required headers.")
            
            raw_data = list(reader)
            
            # Process in chunks
            for chunk in chunk_data(raw_data, chunk_size=50):
                for row in chunk:
                    try:
                        # Validation & Sanitization Pipeline
                        record = MandiPriceData(**row)
                        valid_records.append(record)
                    except ValidationError as e:
                        errors.append({"row": row, "error": str(e)})
                        
    except Exception as e:
        logger.error(f"Ingestion Failed: {str(e)}")
        return None, None
        
    latency = time.time() - start_time
    logger.info(f"Ingestion complete. Valid: {len(valid_records)} | Errors: {len(errors)} | Latency: {latency:.4f}s")
    
    return valid_records, errors
