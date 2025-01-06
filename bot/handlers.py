import asyncio
import random

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, update, message_id, FSInputFile

from services import withdraw_service
from services.crypto_service import CryptoService
from services.image_service import ImageService
from services.password_service import PasswordService
from bot.keyboards import BotKeyboards
from aiogram import types

router = Router()

async def check_if_admin_or_private(event, bot):
    # Determine the chat type and user ID based on the event type
    if isinstance(event, types.Message):
        chat_type = event.chat.type
        user_id = event.from_user.id
        chat_id = event.chat.id
    elif isinstance(event, CallbackQuery):
        chat_type = event.message.chat.type
        user_id = event.from_user.id
        chat_id = event.message.chat.id
    else:
        return False

    if chat_type == 'private':
        return True

    chat_administrators = await bot.get_chat_administrators(chat_id)

    if any(admin.user.id == user_id for admin in chat_administrators):
        return True

    return False

@router.message(Command("start"))
async def start_command(message: Message):
    is_allowed = await check_if_admin_or_private(message, message.bot)

    if not is_allowed:
        await message.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await message.answer(
        "Welcome to the Crypto Stats Bot! Choose an option:",
        reply_markup=BotKeyboards.get_main_menu_keyboard()
    )


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:

        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await callback.message.edit_text(
        "Welcome to the Crypto Stats Bot! Choose an option:",
        reply_markup=BotKeyboards.get_main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "market_stats")
async def market_stats_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await callback.message.edit_text(
        "Market Statistics Menu:",
        reply_markup=BotKeyboards.get_market_stats_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await callback.message.edit_text(
        "Crypto Stats Bot v1.0\n\n"
        "Features:\n"
        "- Real-time Crypto Market Data\n"
        "- Password Generator\n"
        "- Button generation\n\n"
        "[Full Free]\n\n"
        "Created with ❤️ by MP Team",
        reply_markup=BotKeyboards.get_about_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "password_menu")
async def password_menu_callback(callback: CallbackQuery):

    if callback.message.chat.type != 'private':
        await callback.answer("This command can only be used in a private chat with the bot.", show_alert=True)
        return

    await callback.message.edit_text(
        "Password Generator Menu:",
        reply_markup=BotKeyboards.get_password_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "now_command")
async def now_command_callback(callback: CallbackQuery):
    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    # Retrieve various market statistics
    rates = CryptoService.get_crypto_rates()
    fear_and_greed_value, fear_and_greed_status = CryptoService.get_fear_and_greed_index()
    top_performer = CryptoService.get_top_performer()

    # Calculate alt season index
    alt_season_index = CryptoService.calculate_altcoin_season_index()
    season_visualization, btc_percentage = CryptoService.get_season_visualization(alt_season_index)

    if rates:
        message = (
            f"<b>Current Market:</b> \n\n"
            f"<b>🧮 Bitcoin Dominance:</b> {rates.get('bitcoin_dominance', 'N/A')}% \n"
            f"<b>😱 Fear and Greed Index:</b> {fear_and_greed_value} ({fear_and_greed_status}) \n\n"
            f"<b>Season:</b> [{btc_percentage}/{100 - btc_percentage}] \n\n"
            f"{season_visualization} \n\n"
            f"<b>🚀 Top Performer (24h):</b>\n {top_performer['name']} ({top_performer['symbol']}) +{top_performer['change_24h']:.2f}%"
        )

        image_path = ImageService.create_image(rates)
        if image_path:

            photo = FSInputFile(image_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=message,
                parse_mode='HTML'
            )
    else:
        await callback.message.answer("There was an error, try again.")

    await callback.message.answer(
        "Market Statistics Menu:",
        reply_markup=BotKeyboards.get_market_stats_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "top_performer")
async def top_performer_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    top_performer = CryptoService.get_top_performer()
    message = (f"🏆 Top Performer in 24h:\n"
               f"Name: {top_performer['name']} ({top_performer['symbol']})\n"
               f"Price: ${top_performer['price']}\n"
               f"24h Change: {top_performer['change_24h']:.2f}%")
    await callback.message.edit_text(
        text=message,
        reply_markup=BotKeyboards.get_market_stats_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("passgen_"))
async def passgen_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    count = int(callback.data.split("_")[1])
    passwords = [PasswordService.generate_password() for _ in range(count)]

    message = "🔐 Generated Passwords:\n\n"
    for i, password in enumerate(passwords, 1):
        strength = PasswordService.check_password_strength(password)
        message += (f"<code>{password}</code>\n")

    await callback.message.edit_text(
        text=message,
        parse_mode='HTML',
        reply_markup=BotKeyboards.get_password_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "gen_button")
async def top_performer_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    message = "📊 Press the button to get stats: \n\n<i>[Pin this message]</i>"

    await callback.message.edit_text(
        text=message,
        parse_mode='HTML',
        reply_markup=BotKeyboards.gen_button_keyboard()
    )

    await asyncio.sleep(1)
    await start_command(callback.message)

@router.callback_query(F.data == "gen_button_stats")
async def gen_stats_callback(callback: CallbackQuery):
    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    # Retrieve various market statistics
    rates = CryptoService.get_crypto_rates()
    fear_and_greed_value, fear_and_greed_status = CryptoService.get_fear_and_greed_index()
    top_performer = CryptoService.get_top_performer()

    # Calculate alt season index
    alt_season_index = CryptoService.calculate_altcoin_season_index()
    season_visualization, btc_percentage = CryptoService.get_season_visualization(alt_season_index)

    if rates:
        message = (
            f"<b>Current Market:</b> \n\n"
            f"<b>🧮 Bitcoin Dominance:</b> {rates.get('bitcoin_dominance', 'N/A')}% \n"
            f"<b>😱 Fear and Greed Index:</b> {fear_and_greed_value} ({fear_and_greed_status}) \n\n"
            f"<b>Season:</b> [{btc_percentage}/{100 - btc_percentage}] \n\n"
            f"{season_visualization} \n\n"
            f"<b>🚀 Top Performer (24h):</b>\n {top_performer['name']} ({top_performer['symbol']}) +{top_performer['change_24h']:.2f}%"
        )

        image_path = ImageService.create_image(rates)
        if image_path:
            photo = FSInputFile(image_path)
            await callback.message.answer_photo(
                photo=photo,
                caption=message,
                parse_mode='HTML',
                reply_markup=BotKeyboards.simple_menu_keyboard()
            )
    else:
        await callback.message.answer("There was an error, try again.")

    await callback.answer()

@router.callback_query(F.data == "simple_menu")
async def simple_menu_callback(callback: CallbackQuery):

    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await start_command(callback.message)


class WithdrawStates(StatesGroup):
    exchange = State()
    proxy = State()
    api_key = State()
    api_secret = State()
    api_passphrase = State()
    token = State()
    network = State()
    shuffle_wallets = State()
    amount_selection_type = State()
    amount_range = State()
    fixed_amount = State()
    wallets_file = State()


# Add this method to the existing handlers
@router.callback_query(F.data == "withdraw_menu")
async def withdraw_menu_callback(callback: CallbackQuery):
    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    await callback.message.edit_text(
        "Withdrawal Menu: Select an Exchange",
        reply_markup=BotKeyboards.get_withdraw_exchange_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("withdraw_binance"))
@router.callback_query(F.data.startswith("withdraw_okx"))
@router.callback_query(F.data.startswith("withdraw_gate"))
@router.callback_query(F.data.startswith("withdraw_kucoin"))
@router.callback_query(F.data.startswith("withdraw_mexc"))
@router.callback_query(F.data.startswith("withdraw_huobi"))
async def withdraw_exchange_selection(callback: CallbackQuery, state: FSMContext):
    is_allowed = await check_if_admin_or_private(callback, callback.bot)

    if not is_allowed:
        await callback.answer("You are not an admin and cannot use this button.", show_alert=True)
        return

    exchange = callback.data.split("_")[1]
    await state.update_data(exchange=exchange)

    await callback.message.edit_text(
        f"Selected Exchange: {exchange.upper()}\n\n"
        "Please send me the proxy server URL in the format:\n"
        "http://login:password@IP:port"
    )
    await state.set_state(WithdrawStates.proxy)
    await callback.answer()


@router.message(WithdrawStates.proxy)
async def process_proxy(message: Message, state: FSMContext):
    proxy = message.text.strip()
    await state.update_data(proxy=proxy)

    await message.answer(
        "Proxy set successfully. Now, please send me the API Key."
    )
    await state.set_state(WithdrawStates.api_key)


@router.message(WithdrawStates.api_key)
async def process_api_key(message: Message, state: FSMContext):
    api_key = message.text.strip()
    await state.update_data(api_key=api_key)

    await message.answer(
        "API Key set. Now, please send me the API Secret."
    )
    await state.set_state(WithdrawStates.api_secret)


@router.message(WithdrawStates.api_secret)
async def process_api_secret(message: Message, state: FSMContext):
    api_secret = message.text.strip()
    await state.update_data(api_secret=api_secret)

    data = await state.get_data()
    exchange = data['exchange']

    # Check if the exchange requires a passphrase
    if exchange in ['okx', 'kucoin']:
        await message.answer(
            f"{exchange.upper()} requires an API Passphrase. Please send it."
        )
        await state.set_state(WithdrawStates.api_passphrase)
    else:
        await message.answer(
            "Select a token for withdrawal:",
            reply_markup=BotKeyboards.get_withdraw_token_keyboard()
        )
        await state.set_state(WithdrawStates.token)


@router.message(WithdrawStates.api_passphrase)
async def process_api_passphrase(message: Message, state: FSMContext):
    api_passphrase = message.text.strip()
    await state.update_data(api_passphrase=api_passphrase)

    await message.answer(
        "Select a token for withdrawal:",
        reply_markup=BotKeyboards.get_withdraw_token_keyboard()
    )
    await state.set_state(WithdrawStates.token)


@router.callback_query(F.data.startswith("withdraw_token_"))
async def process_token(callback: CallbackQuery, state: FSMContext):
    token = callback.data.split("_")[2]
    await state.update_data(token=token)

    await callback.message.edit_text(
        f"Selected Token: {token}\n\n"
        "Select the network for withdrawal:",
        reply_markup=BotKeyboards.get_withdraw_network_keyboard()
    )
    await state.set_state(WithdrawStates.network)

network_mapping = {
    'arbitrum': 'ARBONE',
    'erc20': 'ERC20',
    'avaxc': 'AVAXC',
    'usdt-avaxc': 'AVAXC',
    'trc20': 'TRC20',
    # Add other mappings as needed
}


@router.callback_query(F.data.startswith("withdraw_network_"))
async def process_network(callback: CallbackQuery, state: FSMContext):
    network = callback.data.split("_")[2]
    # Получаем корректное имя сети для OKX
    okx_network = network_mapping.get(network, network)
    if okx_network not in network_mapping.values():
        print(f"Ошибка: Не найдена сеть {network} для вывода.")
        return

    await state.update_data(network=okx_network)
    await callback.message.edit_text(
        f"Выбранная сеть: {okx_network}\n\n"
        "Продолжить выбор кошельков?",
        reply_markup=BotKeyboards.get_shuffle_wallets_keyboard()
    )
    await state.set_state(WithdrawStates.shuffle_wallets)


@router.callback_query(F.data.startswith("withdraw_shuffle_"))
async def process_shuffle(callback: CallbackQuery, state: FSMContext):
    shuffle = callback.data.split("_")[2]
    await state.update_data(shuffle_wallets=shuffle)

    await callback.message.edit_text(
        "Choose how you want to specify the withdrawal amount:",
        reply_markup=BotKeyboards.get_amount_selection_keyboard()
    )
    await state.set_state(WithdrawStates.amount_selection_type)
    await callback.answer()


# New handler for amount selection type
@router.callback_query(F.data.startswith("withdraw_amount_"))
async def process_amount_selection_type(callback: CallbackQuery, state: FSMContext):
    amount_type = callback.data.split("_")[2]
    await state.update_data(amount_selection_type=amount_type)

    if amount_type == "range":
        await callback.message.edit_text(
            "Send the amount range for withdrawal.\n"
            "Format: min_amount,max_amount (e.g., 1.5-2.5)"
        )
        await state.set_state(WithdrawStates.amount_range)
    elif amount_type == "fixed":
        await callback.message.edit_text(
            "Send the fixed amount for withdrawal.\n"
            "Format: amount (e.g., 2.0)"
        )
        await state.set_state(WithdrawStates.fixed_amount)

    await callback.answer()


# Modified handler for amount range
@router.message(WithdrawStates.amount_range)
async def process_amount_range(message: Message, state: FSMContext):
    amount_range = message.text.strip().split('-')
    if len(amount_range) != 2:
        await message.answer("Invalid format. Please use min-max (e.g., 1.5-2.5)")
        return

    try:
        min_amount = float(amount_range[0])
        max_amount = float(amount_range[1])
        await state.update_data(amount_range=[min_amount, max_amount])

        await message.answer(
            "Now, send me a text file with wallet addresses (one address per line)."
        )
        await state.set_state(WithdrawStates.wallets_file)
    except ValueError:
        await message.answer("Invalid amount. Please enter numeric values.")


# New handler for fixed amount
@router.message(WithdrawStates.fixed_amount)
async def process_fixed_amount(message: Message, state: FSMContext):
    try:
        fixed_amount = float(message.text.strip())
        await state.update_data(fixed_amount=fixed_amount)

        await message.answer(
            "Now, send me a text file with wallet addresses (one address per line)."
        )
        await state.set_state(WithdrawStates.wallets_file)
    except ValueError:
        await message.answer("Invalid amount. Please enter a numeric value.")


# Modified wallets file handler to support both range and fixed amount
@router.message(WithdrawStates.wallets_file)
async def process_wallets_file(message: Message, state: FSMContext):
    wallets = []

    if message.document:
        # File upload method
        file = await message.bot.get_file(message.document.file_id)
        wallets_file = await message.bot.download_file(file.file_path)
        wallets = wallets_file.read().decode('utf-8').splitlines()
    else:
        # Direct message method
        wallets = message.text.strip().split('\n')

    # Clean and validate wallets
    wallets = [wallet.strip() for wallet in wallets if wallet.strip()]

    # Check wallet count
    if len(wallets) > 50:
        await message.answer(
            "Too many wallets! Please send a file with wallet addresses or send up to 50 wallets in a single message.")
        return

    await state.update_data(wallets=wallets)

    # Prepare withdrawal configuration
    data = await state.get_data()

    # Create config message based on amount selection type
    if data.get('amount_selection_type') == 'range':
        config_message = (
            "Withdrawal Configuration:\n"
            f"Exchange: {data['exchange']}\n"
            f"Proxy: {data['proxy']}\n"
            f"Token: {data['token']}\n"
            f"Network: {data['network']}\n"
            f"Shuffle Wallets: {data['shuffle_wallets']}\n"
            f"Amount Range: {data['amount_range'][0]} - {data['amount_range'][1]} {data['token']}\n"
            f"Wallets: {len(data['wallets'])} addresses"
        )
    else:
        config_message = (
            "Withdrawal Configuration:\n"
            f"Exchange: {data['exchange']}\n"
            f"Proxy: {data['proxy']}\n"
            f"Token: {data['token']}\n"
            f"Network: {data['network']}\n"
            f"Shuffle Wallets: {data['shuffle_wallets']}\n"
            f"Fixed Amount: {data['fixed_amount']} {data['token']}\n"
            f"Wallets: {len(data['wallets'])} addresses"
        )

    await message.answer(config_message)

    try:
        # Dynamically set global variables in withdraw_service
        withdraw_service.switch_cex = data['exchange']
        withdraw_service.symbolWithdraw = data['token']
        withdraw_service.network = data['network']
        withdraw_service.proxy_server = data['proxy']
        withdraw_service.shuffle_wallets = data['shuffle_wallets']

        if data.get('amount_selection_type') == 'range':
            withdraw_service.amount = data['amount_range']
        else:
            withdraw_service.amount = [data['fixed_amount'], data['fixed_amount']]

        # Set API credentials dynamically
        if data['exchange'] == 'binance':
            withdraw_service.API.binance_apikey = data['api_key']
            withdraw_service.API.binance_apisecret = data['api_secret']
        elif data['exchange'] == 'okx':
            withdraw_service.API.okx_apikey = data['api_key']
            withdraw_service.API.okx_apisecret = data['api_secret']
            withdraw_service.API.okx_passphrase = data['api_passphrase']
        elif data['exchange'] == 'kucoin':
            withdraw_service.API.kucoin_apikey = data['api_key']
            withdraw_service.API.kucoin_apisecret = data['api_secret']
            withdraw_service.API.kucoin_passphrase = data['api_passphrase']
        # Add similar conditions for other exchanges

        # Perform withdrawals
        numbered_wallets = withdraw_service.shuffle(data['wallets'], data['shuffle_wallets'])

        await message.answer("Starting withdrawals... This might take some time.")

        for wallet_number, address in numbered_wallets:
            amount_to_withdrawal = round(random.uniform(withdraw_service.amount[0], withdraw_service.amount[1]), 2)
            withdraw_service.choose_cex(address, amount_to_withdrawal, wallet_number)
            await asyncio.sleep(random.randint(35, 85))  # Delay between withdrawals

        await message.answer("Withdrawals completed.", reply_markup=BotKeyboards.simple_menu_keyboard())

    except Exception as e:
        await message.answer(f"An error occurred during withdrawals: {str(e)}")

    # Clear the state
    await state.clear()