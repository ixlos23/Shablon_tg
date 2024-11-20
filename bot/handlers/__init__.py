from bot.dispatcher import dp
from bot.handlers.private.product import product_router
from bot.handlers.start import main_router

dp.include_routers(*[
    main_router,
    product_router,
])