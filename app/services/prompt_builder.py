import json
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.schemas.product import PreparedProduct


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


def build_prompts(product: PreparedProduct) -> list:
    data = product.model_dump(exclude={"warnings"}, exclude_none=True)

    data["specs"] = {
        key: value
        for key, value in data["specs"].items()
        if value is not None
        and not (isinstance(value, str) and not value.strip())
    }

    system = (PROMPTS_DIR / "system.txt").read_text(encoding="utf-8")
    user = (PROMPTS_DIR / "user.txt").read_text(encoding="utf-8")

    user = user.replace(
        "{warnings}",
        json.dumps(
            [warning.model_dump(mode="json") for warning in product.warnings],
            ensure_ascii=False,
        ),
    )
    user = user.replace(
        "{product_data}",
        json.dumps(data, ensure_ascii=False),
    )

    return [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]