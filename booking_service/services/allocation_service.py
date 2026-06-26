from abc import ABC, abstractmethod

class AllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, artist: dict, concert: dict) -> dict:
        pass

class BalancedStrategy(AllocationStrategy):
    def allocate(self, artist: dict, concert: dict) -> dict:
        # artist role must match concert role
        if artist["artistRole"] != concert["artistRole"]:
            return {"status": "Rejected", "reason": "Artist role does not match concert role"}

        # artist must be available
        if not artist["available"]:
            return {"status": "Rejected", "reason": "Artist is not available"}

        # artist must be in same city or same state
        same_city = artist["city"] == concert["concertCity"]
        same_state = artist["state"] == concert["concertState"]
        if not same_city and not same_state:
            return {"status": "Rejected", "reason": "Artist is not in the same city or state"}

        # artist cost must not exceed budget
        if artist["performanceCost"] > concert["budgetAllocated"]:
            return {"status": "Rejected", "reason": "Artist cost exceeds allocated budget"}

        return {"status": "Confirmed", "reason": "All validations passed"}

class AvailabilityStrategy(AllocationStrategy):
    def allocate(self, artist: dict, concert: dict) -> dict:
        # artist role must match concert role
        if artist["artistRole"] != concert["artistRole"]:
            return {"status": "Rejected", "reason": "Artist role does not match concert role"}

        # artist must be available
        if not artist["available"]:
            return {"status": "Rejected", "reason": "Artist is not available"}

        # artist cost must not exceed budget
        if artist["performanceCost"] > concert["budgetAllocated"]:
            return {"status": "Rejected", "reason": "Artist cost exceeds allocated budget"}

        return {"status": "Confirmed", "reason": "All validations passed"}

class StrategyFactory:
    @staticmethod
    def get_strategy(strategy_type: str) -> AllocationStrategy:
        strategy = strategy_type.strip().upper()
        if strategy == "BALANCED":
            return BalancedStrategy()
        elif strategy == "AVAILABILITY":
            return AvailabilityStrategy()
        else:
            raise ValueError(f"Invalid strategy type: {strategy}")
