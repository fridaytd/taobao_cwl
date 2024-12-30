from app.processes import login, is_logged_in
from seleniumbase import SB
from app.utils.gsheet import worksheet
from app.models.sheet_models import Product
from app.processes import run
from app.utils.paths import USER_DATA_PATH
from app.utils.logger import logger

from gspread.worksheet import Worksheet


def get_run_indexes(sheet: Worksheet) -> list[int]:
    run_indexes = []
    check_col = sheet.col_values(1)
    for idx, value in enumerate(check_col):
        idx += 1
        if isinstance(value, int):
            if value == 1:
                run_indexes.append(idx)
        if isinstance(value, str):
            try:
                int_value = int(value)
            except Exception:
                continue
            if int_value == 1:
                run_indexes.append(idx)

    return run_indexes


with SB(
    uc=True,
    user_data_dir=str(USER_DATA_PATH),
    headless=False,
) as sb:
    sb.activate_cdp_mode("https://taobao.com")
    # time.sleep(10000)
    if not is_logged_in(sb):
        logger.info("You must login")
        login(sb)

    while True:
        run_indexes = get_run_indexes(worksheet)
        logger.info(f"Run index: {run_indexes}")
        for index in run_indexes:
            logger.info(f"Processing: {index}")
            product = Product.get(worksheet, index)

            try:
                run(sb, product)
            except Exception as e:
                logger.exception(e)

            sb.cdp.sleep(2)
