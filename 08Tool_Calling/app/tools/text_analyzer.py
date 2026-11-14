import re


def text_analyzer(text: str) -> str:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """

    totalChars = len(text)

    words = text.split()
    word_count = len(words)

    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    sentence_count = len(sentences)

    return {
        "character_count": totalChars,
        "word_count": word_count,
        "sentence_count": sentence_count,
    }


analyzer_tool = {
    "type": "function",
    "name": "text_analyzer",
    "description": "Calculate the charactors, words and sentences count for an input",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "text to char,word,sentence count",
            },
        },
        "required": ["text"],
        "additionalProperties": False,
    },
    "strict": True,
}
