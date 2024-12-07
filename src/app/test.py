from app.utils.logger import logger
from app.utils.gsheet import worksheet
from app.models.sheet_models import Product

p = Product.get(worksheet, index=5)

p.Seller = "Dang Tran"
p.update()
print(p.model_dump_json())
