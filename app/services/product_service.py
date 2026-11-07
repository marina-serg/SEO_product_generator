from app.schemas.product import (
    ProductInput,
    PreparedProduct,
    ProductWarning,
    WarningCode,
)


def prepare_product(product: ProductInput) -> PreparedProduct:
    warnings = []

    for field, code in [
        ("manufacturer", WarningCode.MISSING_MANUFACTURER),
        ("description", WarningCode.MISSING_DESCRIPTION),
        ("specs", WarningCode.MISSING_SPECS),
    ]:
        if not getattr(product, field):
            warnings.append(ProductWarning(code=code, field=field))


    return PreparedProduct(
        **product.model_dump(),
        warnings=warnings,
    )