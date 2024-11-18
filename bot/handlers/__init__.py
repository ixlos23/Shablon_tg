from bot.dispatcher import dp
from bot.handlers.start import main_router

dp.include_routers(*[
    main_router,
])