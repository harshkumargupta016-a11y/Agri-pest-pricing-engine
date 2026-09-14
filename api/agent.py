from typing import Any


class PestVisionAgent:
    """Small deterministic workflow used by the API and benchmark script."""

    def __init__(self) -> None:
        self.state = "IDLE"
        self.total_tokens_used = 0

    def vector_search(self, query: str) -> str:
        self.state = "SEARCHING_VECTORS"
        return f"Treatment recommendation for {query}: Tebuconazole"

    def _simulate_external_llm_call(self, context: str) -> str:
        self.total_tokens_used += len(context.split())
        return "Diagnosis completed with external provider."

    def process_diagnosis_workflow(self, image_data: str) -> dict[str, Any]:
        self.state = "PROCESSING"
        context = self.vector_search(image_data)

        try:
            advice = self._simulate_external_llm_call(context)
        except (ConnectionError, TimeoutError) as error:
            advice = f"FALLBACK TRIGGERED: {error}"

        self.state = "COMPLETED"
        return {
            "status": "success",
            "workflow_state": self.state,
            "data": {
                "final_advice": advice,
                "session_tokens_used": self.total_tokens_used,
            },
        }
