import os
import time as t 



def main():
    try:
        btc_id = os.system('python3 ws_binance.py BTCUSDT wss://stream.binance.com:9443/ws/btcusdt@kline_5m &')
        eth_id = os.system('python3 ws_binance.py ETHUSDT wss://stream.binance.com:9443/ws/ethusdt@kline_5m &')
        doge_id = os.system('python3 ws_binance.py DOGEUSDT wss://stream.binance.com:9443/ws/dogeusdt@kline_5m &')
        sol_id = os.system('python3 ws_binance.py SOLUSDT wss://stream.binance.com:9443/ws/solusdt@kline_5m &')
        bnb_id = os.system('python3 ws_binance.py BNBUSDT wss://stream.binance.com:9443/ws/bnbusdt@kline_5m &')
        fx_id = os.system('python3 scraping_fx.py &')
        bot_id = os.system("python3 bot.py &")
        al_id = os.system('python3 check_alerts.py &')
        while True:
            t.sleep(2)
            pass

    except KeyboardInterrupt:
        os.system(f'kill {bot_id}')
        os.system(f'kill {al_id}')
        os.system(f'kill {eth_id}')
        os.system(f'kill {btc_id}')
        os.system(f'kill {doge_id}')
        os.system(f'kill {sol_id}')
        os.system(f'kill {bnb_id}')
        os.system(f'kill {fx_id}')
        raise SystemExit()


if __name__ == '__main__':
    main()