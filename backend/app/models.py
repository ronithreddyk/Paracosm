from typing import Any, Dict, List

from pydantic import BaseModel, field_validator


class RealityRequest(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        prompt = value.strip()

        if len(prompt) < 8:
            raise ValueError("Prompt must contain at least 8 characters.")
        if len(prompt) > 500:
            raise ValueError("Prompt must contain no more than 500 characters.")
        if not any(character.isalnum() for character in prompt):
            raise ValueError("Prompt must contain letters or numbers.")

        return prompt


class RealityResponse(BaseModel):
    reality: Dict[str, Any]
    imagePrompts: List[str]
    images: List[str]
