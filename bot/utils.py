from aiogram.utils.i18n import gettext as _

from db.models import Product


def caption_book(mushk: Product):
    caption = """
{title}: {mushk_name}
{description}: {mushk_description}
{price}: {mushk_price}
    """.format(title=_("🔹 Title") ,
               mushk_name=mushk.title,
               description=_("📖 Description"),
               mushk_description=mushk.description,
               price=_("💸 Price"),
               mushk_price=mushk.price,
               )
    return caption # noqa