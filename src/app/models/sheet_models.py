from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Self
from gspread.worksheet import Worksheet

from app.shared.consts import COL_META_FIELD_NAME
from app.decorators import retry_on_fail


class ColSheetModel(BaseModel):
    # Model config
    model_config = ConfigDict(arbitrary_types_allowed=True)

    worksheet: Worksheet = Field(exclude=True)
    index: int

    @classmethod
    def mapping_fields(cls) -> dict:
        mapping_fields = {}
        for field_name, field_info in cls.model_fields.items():
            if hasattr(field_info, "metadata"):
                for metadata in field_info.metadata:
                    if COL_META_FIELD_NAME in metadata:
                        mapping_fields[field_name] = metadata[COL_META_FIELD_NAME]
                        break

        return mapping_fields

    @classmethod
    def get(
        cls,
        worksheet: Worksheet,
        index: int,
    ) -> Self:
        mapping_dict = cls.mapping_fields()

        query_value = []

        for _, v in mapping_dict.items():
            query_value.append(f"{v}{index}")

        model_dict = {
            "index": index,
            "worksheet": worksheet,
        }

        query_results = worksheet.batch_get(query_value)
        count = 0
        for k, _ in mapping_dict.items():
            model_dict[k] = query_results[count].first()
            if isinstance(model_dict[k], str):
                model_dict[k] = model_dict[k].strip()
            count += 1
        return cls.model_validate(model_dict)

    @retry_on_fail()
    def update(
        self,
    ) -> None:
        mapping_dict = self.mapping_fields()
        model_dict = self.model_dump(mode="json")

        update_batch = []
        for k, v in mapping_dict.items():
            update_batch.append(
                {
                    "range": f"{v}{self.index}",
                    "values": [[model_dict[k]]],
                }
            )

        self.worksheet.batch_update(update_batch)


class Product(ColSheetModel):
    CHECK: Annotated[int, {COL_META_FIELD_NAME: "A"}]
    Product_name: Annotated[str, {COL_META_FIELD_NAME: "B"}]
    Product_link: Annotated[str, {COL_META_FIELD_NAME: "C"}]
    Selection_1: Annotated[str | None, {COL_META_FIELD_NAME: "D"}] = None
    Selection_2: Annotated[str | None, {COL_META_FIELD_NAME: "E"}] = None
    Selection_3: Annotated[str | None, {COL_META_FIELD_NAME: "F"}] = None
    Price: Annotated[float | None, {COL_META_FIELD_NAME: "G"}] = None
    Seller: Annotated[str | None, {COL_META_FIELD_NAME: "H"}] = None
    Last_update: Annotated[str | None, {COL_META_FIELD_NAME: "I"}] = None
    Note: Annotated[str | None, {COL_META_FIELD_NAME: "J"}] = None
