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

def main(flow):
    driver_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
    users = utils.load_account("account.json")

    for user in users:
        driver = get_driver(driver_path)
        start_new_session(driver)
        for game in flow:
            game(driver, user)
        stop_session(driver)

def start_new_session(driver):
    driver.get(MABINOGI_URL)

def stop_session(driver):
    driver.close()

def get_driver(driver_path):
    driver = webdriver.Chrome(driver_path)
    return driver

def login(driver, user):
    # Use dice game as login entry page
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mabinogi 13th')

    args = parser.parse_args()

    game = {
        "login": login,
        "feed_plant": feed_plant,
        "flower_lottery": flower_lottery
    }

    main([game['login'], game['feed_plant']])