from datetime import datetime
import random

from bs4 import BeautifulSoup

from app.utils.logger import logger
from app.models.sheet_models import Product
from app.models.crwl_model import CrProduct
from app.crwl import is_error_page, whether_need_to_click, extract_info
from app.shared.exceptions import AppError


def sb_sleep_random(sb, min: float = 1, max: float = 3):
    sb.cdp.sleep(random.uniform(min, max))


def is_logged_in(
    sb,
) -> bool:
    try:
        a_info_nick = sb.cdp.locator("a.site-nav-login-info-nick", timeout=3)
        if a_info_nick:
            return True
    except Exception:
        pass

    return False


def login(sb):
    url = "https://login.taobao.com"
    # Go to login link
    sb.cdp.get(url)
    while True:
        if is_logged_in(sb):
            break
        sb_sleep_random(sb, 3, 4)

    logger.info("Loggin success")


def crwl_for_one(
    sb,
    product: Product,
) -> CrProduct:
    # Go to product link
    sb.cdp.get(product.Product_link)

    # Get page source and parse to soup
    soup = BeautifulSoup(
        sb.cdp.get_page_source(),
        "html.parser",
    )

    # Check if error page -> link is invalid
    if is_error_page(soup):
        raise AppError("Product link is invalid!!!")

    # Check if login
    if not is_logged_in(sb):
        # Go to login page if no login
        logger.info("Need to login")
        login(sb)

        # Back to product link
        sb.cdp.get(product.Product_link)

    # Sleep random
    sb_sleep_random(sb)

    if product.Selection_1:
        sb_sleep_random(sb, 1, 2)
        soup = BeautifulSoup(
            sb.cdp.get_page_source(),
            "html.parser",
        )
        if whether_need_to_click(soup, product.Selection_1):
            logger.info(f"Click at: {product.Selection_1}")
            tag = sb.cdp.find_element_by_text(product.Selection_1)
            sb_sleep_random(sb)
            tag.click()
        else:
            logger.info(f"{product.Selection_1} is selected already")
    if product.Selection_2:
        sb_sleep_random(sb, 1, 2)
        soup = BeautifulSoup(
            sb.cdp.get_page_source(),
            "html.parser",
        )
        if whether_need_to_click(soup, product.Selection_2):
            logger.info(f"Click at: {product.Selection_2}")
            tag = sb.cdp.find_element_by_text(product.Selection_2)
            sb_sleep_random(sb)
            tag.click()
        else:
            logger.info(f"{product.Selection_2} is selected already")
    if product.Selection_3:
        sb_sleep_random(sb, 1, 2)
        soup = BeautifulSoup(
            sb.cdp.get_page_source(),
            "html.parser",
        )
        if whether_need_to_click(soup, product.Selection_3):
            logger.info(f"Click at: {product.Selection_3}")
            tag = sb.cdp.find_element_by_text(product.Selection_3)
            sb_sleep_random(sb)
            tag.click()
        else:
            logger.info(f"{product.Selection_3} is selected already")

    sb_sleep_random(sb, 1, 2)
    soup = BeautifulSoup(
        sb.cdp.get_page_source(),
        "html.parser",
    )
    res = extract_info(soup)
    return res


def last_update_message(
    now: datetime,
) -> str:
    formatted_date = now.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_date


def run(
    sb,
    product: Product,
):
    try:
        crwl_result = crwl_for_one(sb, product)
        now = datetime.now()
        product.Last_update = last_update_message(now)
        product.Price = crwl_result.price
        product.Seller = crwl_result.seller
        product.Note = "Cập nhật thành công"

    except Exception as e:
        now = datetime.now()
        product.Last_update = last_update_message(now)
        product.Note = f"FAILED: {e}"
        logger.exception(e)

    finally:
        logger.info("Sheet updating")
        product.update()
