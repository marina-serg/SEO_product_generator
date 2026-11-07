import logging

from fastapi import APIRouter, HTTPException
from langchain_google_genai.chat_models import (
    GoogleAPIError,
    GoogleInvalidRequestError,
)

from app.schemas.product import ProductInput, GeneratedProduct
from app.services.product_service import prepare_product
from app.services.generation import generate_product


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/generate", response_model=GeneratedProduct)
def create_product(product: ProductInput) -> GeneratedProduct:
    try:
        prepared_product = prepare_product(product)
        return generate_product(prepared_product)

    except GoogleInvalidRequestError as exc:
        logger.exception("Invalid request to Gemini")
        raise HTTPException(
            status_code=502,
            detail="Не удалось сформировать корректный запрос к модели.",
        ) from exc

    except GoogleAPIError as exc:
        logger.exception("Gemini API error")
        raise HTTPException(
            status_code=503,
            detail="Сервис генерации временно недоступен. Попробуйте позже.",
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected error during product generation")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера.",
        ) from exc