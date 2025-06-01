import base64

def blob_to_base64(blob_data: bytes) -> str:
    if not blob_data:
        return None
    return base64.b64encode(blob_data).decode("utf-8")
