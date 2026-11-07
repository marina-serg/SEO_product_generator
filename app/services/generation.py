import logging

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings
from app.schemas.product import GeneratedProduct, PreparedProduct
from app.services.prompt_builder import build_prompts


logger = logging.getLogger(__name__)


llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.gemini_api_key,
    temperature=0,
    timeout=settings.gemini_timeout,
    max_retries=settings.max_retries,
)

generator = llm.with_structured_output(GeneratedProduct)

def generate_product(product: PreparedProduct) -> GeneratedProduct:
    logger.info("Начало генерации SEO-карточки товара")

    try:
        result = generator.invoke(build_prompts(product))
        logger.info("SEO-карточка товара успешно сгенерирована")
        return result

    except Exception:
        logger.exception("Ошибка генерации SEO-карточки товара")
        raise