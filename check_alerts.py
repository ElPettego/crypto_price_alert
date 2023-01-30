import db 
import time as t
import alert
import auth

ALERT_DB = db.DB()

def main():
    while True:
        print('CHECKING ALERTS...')
        alerts = ALERT_DB.get_alerts()
        # print(type(alerts))
        for al in alerts:
            # print(type(al), al)
            auth_ses = auth.AUTH()
            if not auth_ses.is_user_auth(chat_id=al['chat_id']):
                continue
            curr_alert = alert.Alert(
                current_price=al['open_price'],
                target_price=al['target_price'],
                current_date=al['open_date'],
                assett_tag=al['assett_tag'],
                chat_id=al['chat_id'])
            curr_alert.check_alert()
        t.sleep(30)

if __name__ == '__main__':
    main()