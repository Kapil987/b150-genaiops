from __future__ import annotations

import asyncio
import json
import os
import re
from typing import Any

import boto3


class BedrockJsonClient:
    def __init__(self, model_id: str | None = None, region: str | None = None) -> None:
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "amazon.nova-micro-v1:0")
        self.region = (
            region
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or "us-east-1"
        )
        self.client = boto3.client("bedrock-runtime", region_name=self.region)

    async def extract_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        text = await asyncio.to_thread(self._call_model, system_prompt, user_prompt)
        return self._parse_json_or_fail(text)

    def _call_model(self, system_prompt: str, user_prompt: str) -> str:
        resp = self.client.converse(
            modelId=self.model_id,
            system=[{"text": system_prompt}],
            messages=[{"role": "user", "content": [{"text": user_prompt}]}],
            inferenceConfig={"temperature": 0, "maxTokens": 2048},
        )
        parts = resp["output"]["message"]["content"]
        return "".join(p.get("text", "") for p in parts)

    @staticmethod
    def _parse_json_or_fail(text: str) -> dict[str, Any]:
        if not text:
            raise ValueError("LLM returned empty response.")
        try:
            return json.loads(text)
        except Exception:
            pass

        match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.S)
        if match:
            return json.loads(match.group(1))

        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start : end + 1])

        raise ValueError("LLM output is not valid JSON.")

