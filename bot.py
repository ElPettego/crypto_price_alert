from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime as dt
import time as t
import config as cfg
import db 
import auth

WELCOME = """đ WELCOME TO TRADING PRICE ALERT BOT!!! đ¤

"""

USAGE = """đ§ USAGE: 
âšī¸ INFO: <> is used for passing an argument to the command

/start <password> => STARTS THE BOT. FOR THE PASSWORD ASK @uomo_succo. EXAMPLE => /start password

/help => DISPLAYS THIS MESSAGE

/set_alert <asset> <price> => CREATE A NEW ALERT. <assett> is one of the assets in the belove list. <price> is the target price of the alarm. EXAMPLE => /set_alert BTCUSDT 100000

/get_alert => SHOWS ACTIVE ALERTS

/delete_alert <index> => DELETE ONE OF THE ACTIVE ALERTS. type /get_alert to show active alerts and then /delete_alert <index> to delete the alert. EXAMPLE => /delete_alert 1

/get_price <asset> => GETS THE CURRENT PRICE OF THE ASSET. EXAMPLE => /get_price BTCUSDT

đĒ AVAILABLE ASSETS đĒŖ: 
- BTCUSDT
- ETHUSDT
- DOGEUSDT
- SOLUSDT
- BNBUSDT
- EURUSD
- GBPUSD
- EURGBP

âšī¸ FX PRICES ARE AVAILABLE WITH 4 DECIMALS => 1.2345

đ SEE YOU ON THE MOON đ"""

NOT_AUTH = """â U ARE NOT AUTHENTICATED :(. U MUST ASK THE PASSWORD TO @uomo_succo â"""

ALERT_DB = db.DB()

async def start(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    auth_ses = auth.AUTH()
    chat_id = update.effective_message.chat_id
    try:
        password = context.args[0]
    except IndexError:
        if auth_ses.is_user_auth(chat_id=chat_id):
            await update.effective_message.reply_text(WELCOME+USAGE)
            return
        await update.effective_message.reply_text(NOT_AUTH)
        return
    auth_code, auth_res = auth_ses.auth_user(chat_id=chat_id, password=password)
    if auth_code == 1:
        await update.effective_message.reply_text(WELCOME+USAGE)
        if auth_res == f'USER {chat_id} AUTHED SUCCESFULLY!':
            print('NEW SESSION', chat_id)
        return
    if auth_code == 0:
        await update.effective_message.reply_text(auth_res)
        return


async def set_alert(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    auth_ses = auth.AUTH()
    if not auth_ses.is_user_auth(chat_id=chat_id):
        await update.effective_message.reply_text(NOT_AUTH)
        return
    try:
        assett = str(context.args[0])
        price = abs(float(context.args[1]))
        if assett not in cfg.ASSETS:
            await update.effective_message.reply_text("â ī¸ ASSET NOT AVAILABLE â WRITE TO @uomo_succo IF U WANNA ADD IT :)")
            return
        with open(f'./prices/{assett}.txt', 'r') as f:
            current_price = f.read()
        alert_o = dict(
            open_price=float(current_price),
            target_price=price,
            open_date=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            assett_tag=assett,
            chat_id=chat_id
        )
        ALERT_DB.add_alert(alert=alert_o)
        print(f'ALERT SET SUCCESFULLY! {assett} {price}', chat_id)

        await update.effective_message.reply_text(f"đ¯ ALERT SET SUCCESSFULLY! â")

    except (IndexError, ValueError):
        await update.effective_message.reply_text(USAGE)

async def get_alert(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    auth_ses = auth.AUTH()
    if not auth_ses.is_user_auth(chat_id=chat_id):
        await update.effective_message.reply_text(NOT_AUTH)
        return
    alerts = ALERT_DB.get_alerts(chat_id=chat_id)
    print('ALERTS REQUESTED', chat_id)
    mex = ''
    for ind, alert in enumerate(alerts):
        mex += f'đ¨ ALERT {ind+1}\nđĒ ASSETT => {alert["assett_tag"]} \nđ¯ TARGET => {alert["target_price"]}\nâ˛ī¸ DATE => {alert["open_date"]}\n\n'
    if mex == '':
        await update.effective_message.reply_text('đ NO ACTIVE ALERTS AT THE MOMENT :(')
        return
    await update.effective_message.reply_text(mex)
        

async def delete_alert(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    auth_ses = auth.AUTH()
    if not auth_ses.is_user_auth(chat_id=chat_id):
        await update.effective_message.reply_text(NOT_AUTH)
        return
    alerts = ALERT_DB.get_alerts(chat_id=chat_id)
    try:
        index = int(context.args[0])
    except (IndexError, ValueError):
        await update.effective_message.reply_text(USAGE)
        return
    ALERT_DB.delete_alert(chat_id=chat_id, open_date=alerts[index-1]['open_date'])
    await update.effective_message.reply_text(f'đ¨ ALERT {index} DELETED SUCCESFULLY! đī¸')

async def set_password(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    if chat_id != 960900141:
        await update.effective_message.reply_text('â U CANT ACCESS THIS COMAND BRO!!! â')
        return
    try:
        pw = str(context.args[0])
    except (IndexError, ValueError):
        await update.effective_message.reply_text('WRONG FORMAT BRO!')
        return
    ALERT_DB.set_password(password=pw)
    await update.effective_message.reply_text('PASSWORD CHANGED SUCCESFULLY!!')

async def get_price(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    auth_ses = auth.AUTH()
    if not auth_ses.is_user_auth(chat_id=chat_id):
        await update.effective_message.reply_text(NOT_AUTH)
        return
    try:
        assett = str(context.args[0])
    except (IndexError, ValueError):
        await update.effective_message.reply_text(USAGE)
    if assett not in cfg.ASSETS:
        await update.effective_message.reply_text("â ī¸ ASSET NOT AVAILABLE â WRITE TO @uomo_succo IF U WANNA ADD IT :)")
        return
    with open(f'./prices/{assett}.txt', 'r') as f:
        current_price = f.read()
    await update.effective_message.reply_text(f'đĒ ASSET => {assett}\nđ° PRICE => {current_price}')

def main() -> None:

    application = Application.builder().token(cfg.BOT_TOKEN).build()

    application.add_handler(CommandHandler(['start', 'help'], start))
    application.add_handler(CommandHandler('get_price', get_price))
    application.add_handler(CommandHandler('set_alert', set_alert))
    application.add_handler(CommandHandler('get_alert', get_alert))
    application.add_handler(CommandHandler('delete_alert', delete_alert))
    application.add_handler(CommandHandler('set_password', set_password))

    try:
        application.run_polling()
    except RuntimeError:
        application.shutdown()
    
if __name__ == '__main__':
    main()