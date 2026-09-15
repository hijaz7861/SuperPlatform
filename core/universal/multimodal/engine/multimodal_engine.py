from ..models.multimodal_models import (
    MultimodalInput,
    MultimodalResult,
)


class MultimodalEngine:

    SUPPORTED = {
        "text",
        "image",
        "audio",
        "video",
        "document",
    }

    def process(self, item):
        if item.input_type not in self.SUPPORTED:
            raise ValueError("UNSUPPORTED_MODALITY")

        return MultimodalResult(
            input_id=item.input_id,
            detected_type=item.input_type,
            status="PROCESSED",
            data={
                "provider_independent": True,
                "payload_present": item.payload is not None,
            },
        )

    def create(self, input_id, input_type, payload):
        return MultimodalInput(
            input_id=input_id,
            input_type=input_type,
            payload=payload,
        )
