import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import logging

# 로그 생성
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# GUI 함수
def start_ticketing():
    # 사용자 입력값 가져오기
    concert_id = concert_id_entry.get()
    ticket_count = ticket_count_entry.get()
    wanted_date = wanted_date_entry.get()
    interpark_id = interpark_id_entry.get()
    interpark_pw = interpark_pw_entry.get()

    # 필수 입력 검증
    if not (concert_id.isdigit() and ticket_count.isdigit() and 1 <= int(ticket_count) <= 4):
        messagebox.showerror("입력 오류", "유효한 값을 입력하세요.")
        return

    # 티켓팅 자동화 수행
    try:
        logger.debug("Start automated ticketing!")
        automate_ticketing(concert_id, ticket_count, wanted_date, interpark_id, interpark_pw)
    except Exception as e:
        messagebox.showerror("오류", str(e))


def automate_ticketing(concert_id, ticket_count, wanted_date, interpark_id, interpark_pw):
    # Selenium WebDriver 설정
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-popup-blocking')
    # options.add_argument('--headless')  # 브라우저가 뜨지 않도록 설정

    # Chrome WebDriver 설정
    service = Service(executable_path='/opt/homebrew/bin/chromedriver')  # chromedriver 경로 설정
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    try:
        # 인터파크 로그인 페이지로 이동
        # driver.get("https://ticket.interpark.com/Gate/TPLogin.asp")
        driver.get("https://accounts.interpark.com/login/form")

        # WebDriverWait을 사용하여 요소가 로드될 때까지 대기 (최대 10초)
        wait = WebDriverWait(driver, 10)

        # ID 입력 필드가 로딩될 때까지 대기
        user_id_field = wait.until(EC.presence_of_element_located((By.ID, "userId")))
        user_id_field.send_keys(interpark_id)

        # PW 입력 필드가 로딩될 때까지 대기
        user_pw_field = wait.until(EC.presence_of_element_located((By.ID, "userPwd")))
        user_pw_field.send_keys(interpark_pw)

        # 로그인 버튼이 로딩될 때까지 대기
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btn_login")))
        login_button.click()

        # 로그인 완료 후 콘서트 페이지로 이동
        driver.get(f"https://tickets.interpark.com/goods/{concert_id}")

        # # 팝업 닫기 버튼을 대기 후 닫기
        close_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "popupCloseBtn")))
        
        for button in close_buttons:
            # button.click()
            # button.send_keys(Keys.ENTER)
            driver.execute_script("arguments[0].click();", button)

        # 날짜 선택 대기 및 클릭
        date_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//li[text()='{wanted_date}']")))
        for date_element in date_elements:
            if "disabled" not in date_element.get_attribute("class"):
                # date_element.click()
                driver.execute_script("arguments[0].click();", date_element)
                break

        # 예매하기 버튼이 클릭 가능할 때까지 대기
        reserve_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.sideBtn.is-primary span")))
        # reserve_button.click()
        driver.execute_script("arguments[0].click();", reserve_button)

        # 새 창으로 전환
        wait_for_new_window_and_switch(driver)

        # 새 창에서 '잠깐 접어두기' 버튼 처리
        wait_for_captcha(driver)

        # 좌석 선택
        select_seats(driver, ticket_count)

    finally:
        driver.quit()

# 새 창 대기 및 전환 함수
def wait_for_new_window_and_switch(driver):
    # 기존 창 핸들 저장
    original_window = driver.current_window_handle

    # 새 창이 열릴 때까지 대기
    WebDriverWait(driver, 10).until(EC.new_window_is_opened)

    # 모든 창 핸들 목록 가져오기
    windows = driver.window_handles

    # 새 창으로 전환
    for window in windows:
        if window != original_window:
            driver.switch_to.window(window)
            break

# 대기열 처리 함수
def wait_for_captcha(driver):
    # 'divCaptchaFolding'이 로드될 때까지 대기
    wait = WebDriverWait(driver, 60)
    captcha_folding = wait.until(EC.presence_of_element_located((By.ID, "divCaptchaFolding")))

    # '잠깐 접어두기' 링크 클릭
    folding_link = captcha_folding.find_element(By.LINK_TEXT, "잠깐 접어두기")
    driver.execute_script("arguments[0].click();", folding_link)

# 좌석 선택 함수
def select_seats(driver, ticket_count):
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.XPATH, "//b[contains(text(), '좌석배치도입니다')]")))

    seat_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'SeatN')]")
    for seat_element in seat_elements[:int(ticket_count)]:
        seat_element.click()

    # 좌석 선택 완료 버튼 클릭
    driver.find_element(By.ID, "NextStepImage").click()


# GUI 구성
root = tk.Tk()
root.title("인터파크 티켓팅")

tk.Label(root, text="콘서트 ID:").grid(row=0, column=0)
concert_id_entry = tk.Entry(root)
concert_id_entry.grid(row=0, column=1)

tk.Label(root, text="티켓 개수 (1~4):").grid(row=1, column=0)
ticket_count_entry = tk.Entry(root)
ticket_count_entry.grid(row=1, column=1)

tk.Label(root, text="원하는 날짜 (숫자만):").grid(row=2, column=0)
wanted_date_entry = tk.Entry(root)
wanted_date_entry.grid(row=2, column=1)

tk.Label(root, text="인터파크 ID:").grid(row=3, column=0)
interpark_id_entry = tk.Entry(root)
interpark_id_entry.grid(row=3, column=1)

tk.Label(root, text="인터파크 PW:").grid(row=4, column=0)
interpark_pw_entry = tk.Entry(root, show="*")
interpark_pw_entry.grid(row=4, column=1)

start_button = tk.Button(root, text="Start", command=start_ticketing)
start_button.grid(row=5, column=1)

root.mainloop()








# pip install pyinstaller
# pyinstaller --onefile --windowed ticketing.py
# brew install python-tk
# https://jessymin.github.io/web-scraping/2019/10/01/selenium-chrome-binary-error-solution.html -> 크롬 안될때
# https://aquil.tistory.com/9 -> 크롬 안될때

# To start selenium-server now and restart at login:
#   brew services start selenium-server
# Or, if you don't want/need a background service you can just run:
#   /opt/homebrew/opt/selenium-server/bin/selenium-server standalone --port 4444

# pip3 install selenium --break-system-packages