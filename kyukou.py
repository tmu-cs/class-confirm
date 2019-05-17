# 今回は動的サイトのためsleep関数を多用する

#encoding:utf-8
import database
import time
import datetime
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from discord_webhook import DiscordWebhook

# 曜日を取得する
def youbi():
    d = datetime.datetime.now()
    return (d.weekday())

# main関数
# ここで実際にスクリーンショットを取ってWebhookでdiscordに送信
def main(id, password, disname):
    # Headless Firefoxを起動させて休講情報のページへ移動
    options = Options()
    options.add_argument('-headless')
    browser = Firefox(executable_path='geckodriver', options=options)       # Firefoxを起動
    browser.set_window_size(1080, 1080)                                     # ウィンドウサイズを調整
    # wait = WebDriverWait(browser, timeout=10)
    # print(id, password)

    # Campus Squareにログインする
    browser.get('http://www.comp.tmu.ac.jp/portal/')
    browser.find_element_by_name("HPB_ROLLOVER1").click()
    browser.find_element_by_id("username").send_keys(id)               # ID
    browser.find_element_by_id("password").send_keys(password)      # Password
    browser.find_element_by_css_selector('button[type="submit"]').click()

    # 休憩
    time.sleep(3)

    # 休講情報のページに飛ぶ
    browser.find_element_by_css_selector('ul[class="link_item"] > li:nth-of-type(4) > span > a').click()

    # 休憩
    time.sleep(0.5)

    # 既読も表示するようにする
    browser.find_element_by_css_selector('div[class="accordion"] > ul > li > a').click()
    browser.find_element_by_id("chkEtrdFlg_1").click()
    browser.find_element_by_css_selector('p[class="action"] > input:nth-of-type(2)').click()

    time.sleep(0.5)

    # スクリーンショットを撮る
    browser.save_screenshot("paper.png")

    # WebhookのURLを取得しゴミを排除する
    URL = database.searchurl(disname)
    URL = URL[2:]
    URL = URL[:-3]
    print(URL)
    # URL = gosh.requestsURL()
    webhook = DiscordWebhook(url = URL, username = 'astpy')

    # 写真を送る
    with open("./paper.png", "rb") as f:
        webhook.add_file(file=f.read(), filename='example.jpg')

    webhook.execute()

