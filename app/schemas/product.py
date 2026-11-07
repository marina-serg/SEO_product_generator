from enum import StrEnum
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StrictBool,
    StrictInt,
    StringConstraints,
    computed_field,
)


class AppModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


NonEmptyString = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=200,
    ),
]

OptionalText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=5000,
    ),
]

TechnicalText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=10000,
    ),
]

SpecValue = (
    Annotated[str, StringConstraints(max_length=1000)]
    | StrictInt
    | FiniteFloat
    | StrictBool
    | None
)


class ProductInput(AppModel):
    name: NonEmptyString

    manufacturer: OptionalText | None = None
    category: OptionalText | None = None
    description: OptionalText | None = None
    technical_documentation: TechnicalText | None = None

    specs: dict[NonEmptyString, SpecValue] = Field(
        default_factory=dict,
        max_length=100,
    )


class WarningCode(StrEnum):
    MISSING_MANUFACTURER = "Не указан производитель"
    MISSING_DESCRIPTION = "Не заполнено описание товара"
    MISSING_SPECS = "Не указаны технические характеристики"



class ProductWarning(AppModel):
    code: WarningCode
    field: NonEmptyString

    @computed_field
    @property
    def message(self) -> str:
        return self.code.value


class PreparedProduct(ProductInput):
    warnings: list[ProductWarning] = Field(default_factory=list)


class GenerationStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    INSUFFICIENT_DATA = "insufficient_data"


class GeneratedProduct(AppModel):
    status: GenerationStatus
    warnings: OptionalText | None
    seo_title: OptionalText | None
    seo_description: OptionalText | None
    characteristics: dict[NonEmptyString, SpecValue]
    search_queries: list[NonEmptyString]
    commercial_text: OptionalText | None