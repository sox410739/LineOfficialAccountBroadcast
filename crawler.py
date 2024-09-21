from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SELENUIM_WAIT_TIME = 10
    
def initailize_driver():
    driverService = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=driverService)
    return driver
    
def login(driver: webdriver.Chrome, url: str):
    LINE_login_button_xpath = '/html/body/div[2]/div/div[3]/div/form/div/input'
    login_by_qr_button_xpath = '//*[@id="app"]/div/div/div/div/div/div[2]/a'
    try:
        driver.get(url)
        LINE_login_button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, LINE_login_button_xpath)))
        LINE_login_button.click()
        login_by_qr_button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, login_by_qr_button_xpath)))
        login_by_qr_button.click()
        
        # wait user to login and scan QR code until the page is redirected to the chat page
        while driver.current_url != f'{url}?status=success':
            time.sleep(1)
    
    except Exception as e:
        print('[Login failed]\n')
        raise e
        
def get_all_user(driver: webdriver.Chrome):
    users_container_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[1]/div/div[2]/div[2]/div'
    users_elements_css = 'h6[data-v-a7f2b37c]'
    try:
        users_container = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, users_container_xpath)))
        users_elements = WebDriverWait(users_container, SELENUIM_WAIT_TIME).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, users_elements_css)))
        # get text from elements
        users = [user.text for user in users_elements]
        print(users)
        return users
        
    except Exception as e:
        print('[Get all user failed]\n')
        raise e
    
def ensure_message_sent(driver: webdriver.Chrome, message: str):
    message_element = None
    while(True):
        date_group = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.position-relative.date-group')))
        messages = WebDriverWait(date_group[-1], SELENUIM_WAIT_TIME).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.chat.chat-text-dark.chat-reverse.chat-primary')))
        message_element = messages[-1]
        chat_text = WebDriverWait(message_element, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.chat-item-text.user-select-text')))
        if chat_text.get_attribute('textContent') == message:
            break
    
    WebDriverWait(message_element, SELENUIM_WAIT_TIME).until(EC.invisibility_of_element((By.CSS_SELECTOR, '.chat-sub > .dropdown > .fas.fa-sync.text-info')))

def switch_to_manual_reply(driver: webdriver.Chrome):
    button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.ID, '__test__switchChatModeButton')))
    if button.get_attribute('textContent') == '使用手動聊天':
        button.click()
    button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.text_to_be_present_in_element((By.ID, '__test__switchChatModeButton'), '結束手動聊天'))
    
def switch_to_auto_reply(driver: webdriver.Chrome):
    button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.ID, '__test__switchChatModeButton')))
    if button.get_attribute('textContent') == '結束手動聊天':
        button.click()
    button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.text_to_be_present_in_element((By.ID, '__test__switchChatModeButton'), '使用手動聊天'))

def send_message(driver: webdriver.Chrome, users: list, message: str):
    users_container_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[1]/div/div[2]/div[2]/div'
    users_elements_css = 'h6[data-v-a7f2b37c]'
    textarea_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[2]/div[3]/div[2]/div[2]/textarea-ex'
    send_button_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[2]/div[3]/div[2]/div[3]/div[2]/input'
    try:
        for user in users:
            users_container = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, users_container_xpath)))
            # get specific user element
            users_elements = WebDriverWait(users_container, SELENUIM_WAIT_TIME).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, users_elements_css)))
            for user_element in users_elements:
                if user_element.text == user:
                    print(f'User {user} found')
                    user_element.click()
                    switch_to_manual_reply(driver)
                    # send message
                    textarea = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, textarea_xpath)))
                    textarea.send_keys(message)
                    send_button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, send_button_xpath)))
                    send_button.click()
                    ensure_message_sent(driver, message)
                    switch_to_auto_reply(driver)
                    break
            
            # raise Exception(f'User {user} not found')    
        
    except Exception as e:
        print('[Send message failed]\n')
        raise e
        
def send_file(driver: webdriver.Chrome, users: list, file_path: str):
    users_container_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[1]/div/div[2]/div[2]/div'
    users_elements_css = 'h6[data-v-a7f2b37c]'
    file_input_xpath = '/html/body/div[2]/div/div[1]/div[1]/main/div/div[2]/div[3]/div[2]/div[3]/div[1]/input'
    file_send_button_xpath = '/html/body/div[2]/div/div[3]/div/div/div[3]/button[1]'
    try:
        for user in users:
            users_container = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, users_container_xpath)))
            # get specific user element
            users_elements = WebDriverWait(users_container, SELENUIM_WAIT_TIME).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, users_elements_css)))
            for user_element in users_elements:
                if user_element.text == user:
                    print(f'User {user} found')
                    user_element.click()
                    # send file
                    file_input = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))
                    # reset file input file path
                    driver.execute_script('arguments[0].value = ""', file_input)
                    file_input.send_keys(file_path)
                    file_send_button = WebDriverWait(driver, SELENUIM_WAIT_TIME).until(EC.presence_of_element_located((By.XPATH, file_send_button_xpath)))
                    file_send_button.click()
                    time.sleep(1)
                    break

            # raise Exception(f'User {user} not found')
        
    except Exception as e:
        print('[Send file failed]\n')
        raise e
        
def login_and_send_message(url: str, message: str):
    driver = initailize_driver()
    login(driver, url)
    users = get_all_user(driver)
    send_message(driver, users, message)

def login_and_send_file(url: str, file_path: str):
    driver = initailize_driver()
    login(driver, url)
    users = get_all_user(driver)
    send_file(driver, users, file_path)
    