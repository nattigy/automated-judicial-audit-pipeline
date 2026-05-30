import base64
import io
import json
import os
import asyncio

from pdf2image import convert_from_path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Handle the typo in key name as a fallback
_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMNI_API_KEY")
client = genai.Client(api_key=_api_key)

EXTRACTION_PROMPT = """You are a UAE bank compliance assistant. Analyze this court order document and extract structured data.

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):

{
  "action": "FREEZE" or "UNFREEZE",
  "subject": {
    "full_name": "string or null",
    "emirates_id": "string or null",
    "passport_number": "string or null",
    "other_ids": []
  },
  "court": {
    "name": "string or null",
    "emirate": "Dubai" | "Abu Dhabi" | "Sharjah" | "Ajman" | "Other" | null
  },
  "case_reference": "string or null",
  "recipient": "string or null",
  "issued_date": "string or null",
  "instructions": "one sentence summary of what the bank must do",
  "effective_immediately": true or false,
  "confidence": 0.95,
  "raw_notes": "any other relevant details"
}

Rules:
- action MUST be exactly "FREEZE" or "UNFREEZE"
- The document is bilingual (Arabic + English) — use both for higher accuracy
- Extract ALL identification numbers (Emirates ID, passport, trade license, etc.)
- If a field is not present, use null
- confidence is your accuracy score from 0.0 to 1.0"""


def _pdf_to_images(pdf_path: str) -> list[bytes]:
    images = convert_from_path(pdf_path, dpi=200)
    result = []
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        result.append(buf.getvalue())
    return result


def _call_gemini(image_bytes_list: list[bytes]) -> str:
    parts = []
    for img_bytes in image_bytes_list:
        parts.append(types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text=EXTRACTION_PROMPT))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=parts,
    )
    return response.text.strip()


def _parse_response(raw: str) -> dict:
    # Strip markdown fences if model wraps in ```json ... ```
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


async def extract_from_pdf(pdf_path: str, filename: str) -> dict:
    loop = asyncio.get_event_loop()

    image_bytes_list = await loop.run_in_executor(None, _pdf_to_images, pdf_path)
    raw_text = await loop.run_in_executor(None, _call_gemini, image_bytes_list)

    result = _parse_response(raw_text)
    result["filename"] = filename
    result["pages"] = len(image_bytes_list)
    return result
