import os
import re
from typing import Any, Dict, List, Optional

import openai

# "sk-" followed by 48 alphanumberic characters
OPENAI_API_KEY_FORMAT = re.compile("^sk-[a-zA-Z0-9]{48}$")
MISSING_API_KEY_ERROR_MESSAGE = """No API key found for OpenAI.
Please set either the OPENAI_API_KEY environment variable or \
openai.api_key prior to initialization.
API keys can be found or created at \
https://platform.openai.com/account/api-keys
"""
INVALID_API_KEY_ERROR_MESSAGE = """Invalid OpenAI API key.
API key should be of the format: "sk-" followed by \
48 alphanumeric characters.
"""
def validate_openai_api_key(
    api_key: Optional[str] = None, api_type: Optional[str] = None
) -> None:
    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY", "") or openai.api_key
    openai_api_type = (
        api_type or os.environ.get("OPENAI_API_TYPE", "") or openai.api_type
    )

    if not openai_api_key:
        raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)
    elif (
        openai_api_type == "open_ai"
        and openai_api_key != "EMPTY"  # Exempt EMPTY key for fastchat/local models
        and not OPENAI_API_KEY_FORMAT.search(openai_api_key)
    ):
        raise ValueError(INVALID_API_KEY_ERROR_MESSAGE)