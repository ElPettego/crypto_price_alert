from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime as dt
import time as t
import config as cfg
import db 
import auth

WELCOME = """🎉 WELCOME TO CRYPTO PRICE ALERT BOT!!! 🤖

"""

USAGE = """🔧 USAGE: 
ℹ️ INFO: <> is used for passing an argument to the command

/start <password> => STARTS THE BOT. FOR THE PASSWORD ASK @uomo_succo. EXAMPLE => /start password

/help => DISPLAYS THIS MESSAGE

/set_alert <assett> <price> => CREATE A NEW ALERT. <assett> is one of the cryptos in the belove list. <price> is the target price of the alarm. EXAMPLE => /set_alert BTCUSDT 100000

/get_alert => SHOWS ACTIVE ALERTS

/delete_alert <index> => DELETE ONE OF THE ACTIVE ALERTS. type /get_alert to show active alerts and then /delete_alert <index> to delete the alert. EXAMPLE => /delete_alert 1

🪙 AVAILABLE ASSETS 🪣: 
- BTCUSDT
- ETHUSDT
- DOGEUSDT
- SOLUSDT
- BNBUSDT
- EURUSD
- GBPUSD
- EURGBP

🌕 SEE YOU ON THE MOON 🚀"""

NOT_AUTH = """⛔ U ARE NOT AUTHENTICATED :(. U MUST ASK THE PASSWORD TO @uomo_succo ❌"""

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
            await update.effective_message.reply_text("⚠️ ASSET NOT AVAILABLE ❌ WRITE TO @uomo_succo IF U WANNA ADD IT :)")
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

        await update.effective_message.reply_text(f"🎯 ALERT SET SUCCESSFULLY! ✅")

    except (IndexError, ValueError):
        await update.effective_message.reply_text(USAGE)

async def get_alert(update : Update, context : ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    auth_ses = auth.AUTH()
    if not auth_ses.is_user_auth(chat_id=chat_id):
        await update.effective_message.reply_text(NOT_AUTH)
        return
    alerts = ALERT_DB.get_alerts(chat_id=chat_id)
    print(alerts, chat_id)
    mex = ''
    for ind, alert in enumerate(alerts):
        mex += f'🚨 ALERT {ind+1}\n🪙 ASSETT => {alert["assett_tag"]} \n🎯 TARGET => {alert["target_price"]}\n⏲️ DATE => {alert["open_date"]}\n\n'
    if mex == '':
        await update.effective_message.reply_text('🛌 NO ACTIVE ALERTS AT THE MOMENT :(')
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
    await update.effective_message.reply_text(f'🚨 ALERT {index} DELETED SUCCESFULLY! 🗑️')



def main() -> None:

    application = Application.builder().token(cfg.BOT_TOKEN).build()

    application.add_handler(CommandHandler(['start', 'help'], start))
    application.add_handler(CommandHandler('set_alert', set_alert))
    application.add_handler(CommandHandler('get_alert', get_alert))
    application.add_handler(CommandHandler('delete_alert', delete_alert))

    try:
        application.run_polling()
    except RuntimeError:
        application.shutdown()
    
if __name__ == '__main__':
    main()