from aiogram.utils.i18n import gettext as _

from db.models import Product


def caption_book(fitchi: Product):
    caption = """
{title}: {fitchi_name}
{description}: {fitchi_description}
{price}: {fitchi_price}
    """.format(title=_("🔹 Title") ,
               fitchi_name=fitchi.title,
               description=_("📖 Description"),
               fitchi_description=fitchi.description,
               price=_("💸 Price"),
               fitchi_price=fitchi.price,
               )
    return caption # noqa