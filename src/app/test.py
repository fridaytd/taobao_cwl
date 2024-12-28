from app.processes import login, is_logged_in
from seleniumbase import SB
from app.utils.gsheet import worksheet
from app.models.sheet_models import Product
from app.processes import run
from app.utils.paths import USER_DATA_PATH
from app.utils.logger import logger

with SB(
    uc=True,
    user_data_dir=str(USER_DATA_PATH),
    headless=False,
) as sb:
    sb.activate_cdp_mode("https://taobao.com")
    if not is_logged_in(sb):
        logger.info("You must login")
        login(sb)

    while True:
        for i in range(5, 11):
            logger.info(f"Processing: {i}")
            product = Product.get(worksheet, i)

            try:
                run(sb, product)
            except Exception as e:
                logger.error(i)
                logger.exception(e)

            sb.cdp.sleep(2)
