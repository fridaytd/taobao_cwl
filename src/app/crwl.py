from bs4 import BeautifulSoup, Tag
import re

from app.shared.exceptions import CrwlError
from app.models.crwl_model import CrProduct

from typing import Final

SELECTED_SIGN: Final[str] = "isSelected"
DISABLE_SIGN: Final[str] = "isDisabled"


def is_error_page(
    soup: BeautifulSoup,
) -> bool:
    error_tag = soup.find(
        attrs={
            "class": "errorPage",
        }
    )
    if error_tag is None:
        return False

    return True


def is_selected_tag(
    selection: str,
    tag: Tag,
) -> bool:
    for class_name in tag.attrs["class"]:
        if SELECTED_SIGN in class_name:
            return True

        elif DISABLE_SIGN in class_name:
            raise CrwlError(f"Selection: {selection} is disabled!!!")

    return False


def whether_need_to_click(
    soup: BeautifulSoup,
    selection: str,
) -> bool:
    """Whether it need to select things in the selections or they are selected. Raise an exception if can't find the selection in soup

    Args:
        soup (BeautifulSoup): soup
        selections (list[str]): a list of sections (button name)

    Returns:
        list[str]: a list of sections need to be selected
    """

    value_item_tag = soup.find(
        attrs={
            "class": re.compile(
                "^valueItem.*",
            )
        },
        string=selection.strip(),
    )

    if isinstance(value_item_tag, Tag):
        if not is_selected_tag(selection, value_item_tag):
            return True
    else:
        raise CrwlError(f"Selection {selection} not found!!!")

    return False


def extract_info(
    soup: BeautifulSoup,
) -> CrProduct:
    shop_name_tag = soup.find(
        attrs={
            "class": re.compile("^shopName.*"),
            "title": re.compile("^.+$"),
        }
    )
    if isinstance(shop_name_tag, Tag):
        shop_name = shop_name_tag.attrs["title"]
    else:
        raise CrwlError("Can't extract shop name")

    price = None
    item_title_tag = soup.find(
        attrs={
            "class": re.compile("^ItemTitle.*"),
        }
    )

    if isinstance(item_title_tag, Tag):
        parent_price_tag = soup.find(
            attrs={"class": re.compile("^displayPrice.*")},
        )

        if isinstance(parent_price_tag, Tag):
            price_tag = parent_price_tag.find(
                attrs={
                    "class": re.compile("^text.*"),
                }
            )

            if isinstance(price_tag, Tag):
                price_tag_txt = price_tag.get_text(strip=True)
                price = float(price_tag_txt)

    if price is None:
        raise CrwlError("Can't extract price")

    return CrProduct(
        seller=shop_name,
        price=price,
    )
