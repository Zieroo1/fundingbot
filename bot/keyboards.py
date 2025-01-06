from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class BotKeyboards:
    @staticmethod
    def get_main_menu_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Market Stats", callback_data="market_stats"),
                InlineKeyboardButton(text="🔐 Password Generator", callback_data="password_menu")
            ],
            [
                InlineKeyboardButton(text="💸 Withdraw", callback_data="withdraw_menu"),
                InlineKeyboardButton(text="♻️ Gen.Button", callback_data="gen_button")
            ],
            [InlineKeyboardButton(text="ℹ️ About", callback_data="about")]
        ])
        return keyboard

    @staticmethod
    def get_about_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Market Stats", callback_data="market_stats"),
                InlineKeyboardButton(text="🔐 Password Generator", callback_data="password_menu")
            ],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        return keyboard

    @staticmethod
    def get_market_stats_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💰 Crypto Rates", callback_data="now_command"),
                InlineKeyboardButton(text="📈 Top Performer", callback_data="top_performer")
            ],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        return keyboard

    @staticmethod
    def get_password_menu_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="5 Passwords", callback_data="passgen_5"),
                InlineKeyboardButton(text="10 Passwords", callback_data="passgen_10")
            ],
            [
                InlineKeyboardButton(text="25 Passwords", callback_data="passgen_25"),
                InlineKeyboardButton(text="50 Passwords", callback_data="passgen_50")
            ],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        return keyboard

    @staticmethod
    def gen_button_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Get stats", callback_data="gen_button_stats")]
        ])
        return keyboard

    @staticmethod
    def simple_menu_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎛 Menu", callback_data="simple_menu")]
        ])
        return keyboard

    @staticmethod
    def get_withdraw_exchange_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Binance", callback_data="withdraw_binance"),
                InlineKeyboardButton(text="OKX", callback_data="withdraw_okx")
            ],
            [
                InlineKeyboardButton(text="Gate.io", callback_data="withdraw_gate"),
                InlineKeyboardButton(text="Kucoin", callback_data="withdraw_kucoin")
            ],
            [
                InlineKeyboardButton(text="MEXC", callback_data="withdraw_mexc"),
                InlineKeyboardButton(text="Huobi", callback_data="withdraw_huobi")
            ],
            [InlineKeyboardButton(text="🔙 Back to Main Menu", callback_data="main_menu")]
        ])
        return keyboard

    @staticmethod
    def get_withdraw_token_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="USDT", callback_data="withdraw_token_USDT"),
                InlineKeyboardButton(text="USDC", callback_data="withdraw_token_USDC")
            ],
            [
                InlineKeyboardButton(text="ETH", callback_data="withdraw_token_ETH"),
                InlineKeyboardButton(text="BTC", callback_data="withdraw_token_BTC")
            ],
            [InlineKeyboardButton(text="🔙 Back to Withdraw Menu", callback_data="withdraw_menu")]
        ])
        return keyboard

    @staticmethod
    def get_withdraw_network_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Arbitrum One", callback_data="withdraw_network_arbitrum"),
                InlineKeyboardButton(text="ERC20", callback_data="withdraw_network_erc20")
            ],
            [
                InlineKeyboardButton(text="AVAXC", callback_data="withdraw_network_usdt-avaxc"),
                InlineKeyboardButton(text="TRC20", callback_data="withdraw_network_trc20")
            ],
            [InlineKeyboardButton(text="🔙 Back to Token Menu", callback_data="withdraw_token")]
        ])
        return keyboard

    @staticmethod
    def get_shuffle_wallets_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Shuffle Wallets", callback_data="withdraw_shuffle_yes"),
                InlineKeyboardButton(text="Keep Order", callback_data="withdraw_shuffle_no")
            ],
            [InlineKeyboardButton(text="🔙 Back to Network Menu", callback_data="withdraw_network")]
        ])
        return keyboard

    @staticmethod
    def get_amount_selection_keyboard():
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Amount Range", callback_data="withdraw_amount_range"),
                InlineKeyboardButton(text="Fixed Amount", callback_data="withdraw_amount_fixed")
            ],
            [InlineKeyboardButton(text="🔙 Back to Shuffle Menu", callback_data="withdraw_shuffle")]
        ])
        return keyboard