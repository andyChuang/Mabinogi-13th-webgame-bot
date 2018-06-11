# coding=UTF-8
import os, argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import utils

MABINOGI_URL = "https://event.beanfun.com/mabinogi/E20180517/index.aspx"

def main(flow, cd_time):
    driver_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

    for user in users:
        driver = get_driver(driver_path)
        start_new_session(driver)
        login(driver, user)
        for game in flow:
            game(driver, user)
        log_out(driver)
        stop_session(driver)
        time.sleep(cd_time)

def start_new_session(driver):
    driver.get(MABINOGI_URL)

def stop_session(driver):
    driver.close()

def get_driver(driver_path):
    driver = webdriver.Chrome(driver_path)
    return driver

def login(driver, user):
    login_entry = driver.execute_script("return $('a[href=\"Register.aspx\"]')[0]")
    login_entry.click()
    login_routine(driver, user)
    time.sleep(3)

def login_routine(driver, user):
    # Login elements is in iframe, should switch to it
    login_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ifmForm1"))
    )
    driver.switch_to_frame(login_iframe)
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn_login"))
    )
    account = driver.find_element_by_id("t_AccountID")
    account.send_keys(user["account"])
    password = driver.find_element_by_id("t_Password")
    password.send_keys(user["password"])
    login_btn.click()

    # Choose game account
    game_account_selector = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ddl_service_account"))
    )
    for option in game_account_selector.find_elements_by_tag_name('option'):
        if option.text == user["game_account"]:
            option.click()
            driver.find_element_by_id("btn_send_service_account").click()
            break

def log_out(driver):
    log_out_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i13"))
    )
    log_out_btn.click()

def feed_plant(driver, user):
    # Find href
    entry = driver.execute_script("return $('a[id=\"i05\"]')[0]")
    entry.click()

    go_feed_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i19"))
    )
    go_feed_btn.click()

    do_feed_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "p02"))
    )
    do_feed_btn.click()

    go_home_btn = driver.execute_script("return $('#p03 > img')[0]")
    go_home_btn.click()

def flower_lottery(driver, user):
    # Find href
    entry = driver.execute_script("return $('a[id=\"i06\"]')[0]")
    entry.click()

    go_lottery_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "i20"))
    )
    go_lottery_btn.click()

    fb_share_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "FBshare"))
    )
    fb_share_btn.click()

    window_before = driver.window_handles[0]
    window_fb = driver.window_handles[1]
    driver.switch_to_window(window_fb)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(fb_info[0]["email"])

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    password_input.send_keys(fb_info[0]["password"])

    fb_login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u_0_0"))
    )
    fb_login_btn.click()

    switch_who_can_see_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u_0_1s"))
    )
    switch_who_can_see_btn.click()

    only_I_can_see_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '只限本人')]"))
    )
    only_I_can_see_div.click()


    publish_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "u_0_1v"))
    )
    publish_btn.click()

    driver.switch_to_window(window_before)

    close_success_popup_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "popup_close"))
    )
    close_success_popup_btn.click()

    go_home_btn = driver.execute_script("return $('#f02 > img')[0]")
    go_home_btn.click()

def filter_ignore_accounts(users, ignore_accts):
    return [x for x in users if x['account'] not in ignore_accts]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mabinogi 13th')
    parser.add_argument('--cd', dest='cd_time', default=0, help='Cd time between accounts (sec.)')
    parser.add_argument('--ignore', dest='ignore_accounts', help='Ignore these accounts in account.json, split by comma')

    args = parser.parse_args()

    game = {
        "feed_plant": feed_plant,
        "flower_lottery": flower_lottery
    }

    users = filter_ignore_accounts(utils.load_json("account.json"), [x.strip() for x in args.ignore_accounts.split(',')])
    fb_info = utils.load_json("fb.json")

    print '%s Mabinogi accounts and %s fb accounts' % (len(users), len(fb_info))
    print fb_info
    print 'Will wait %s seconds between accounts...' % args.cd_time

    main([game['feed_plant'], game['flower_lottery']], args.cd_time)