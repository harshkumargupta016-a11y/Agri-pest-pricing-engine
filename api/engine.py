import logging

logger = logging.getLogger(__name__)

class MandiPricingEngine:
    def __init__(self):
        # Mock database for agricultural pricing
        self.pricing_data = {
            "Wheat": 2275,
            "Rice": 2183,
            "Soybean": 4600
        }

    def get_price(self, commodity: str, state: str, district: str):
        """Retrieves the current Mandi price for a given commodity."""
        price = self.pricing_data.get(commodity, 2000) # Default fallback price
        logger.info(f"Retrieved price for {commodity} in {district}, {state}: ₹{price}/Quintal")
        
        return {
            "commodity": commodity,
            "state": state,
            "district": district,
            "price_inr_per_quintal": price,
            "status": "success"
        }
