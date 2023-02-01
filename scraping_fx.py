import time as t
import undetected_chromedriver as uc
import pyvirtualdisplay as pvd
from selenium.webdriver.common.by import By

XPATH = '/html/body/article/div/div[3]/div/div[3]/div[1]/div/div[3]/span/span[2]'
DISPLAY = pvd.Display(visible=0, size=(800, 600))
OPTIONS = uc.ChromeOptions()
OPTIONS.add_argument("--log-level=3")
# OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])
LINKS = [
    {'tag': 'EURUSD', 'link':'7250-eur-usd'},
    {'tag': 'GBPUSD', 'link':'7350-gbp-usd'},
    {'tag': 'EURGBP', 'link':'7169-eur-gbp'}
]

def main():
    DISPLAY.start()
    DRIVER = uc.Chrome(options=OPTIONS)
    while True:
        for link in LINKS:
        # TAG = sys.argv[1] #'BTCUSDT'
            DRIVER.get(f'https://www.centralcharts.com/en/{link["link"]}')
            t.sleep(1)
            price = DRIVER.find_element(By.XPATH, XPATH).text
            if price == '-':
                continue
            with open(f'./prices/{link["tag"]}.txt', 'w') as f:
                f.write(str(price))
            # print(price, link['tag'])
        t.sleep(62)

if __name__ == '__main__':
    main()
