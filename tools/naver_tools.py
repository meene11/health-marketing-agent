"""네이버 블로그 Selenium 자동 발행 - auto-multi-agent 검증 코드 재활용."""

import re
import time
import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import settings


def _extract_blog_id(blog_id_or_url: str) -> str:
    return blog_id_or_url.rstrip("/").split("/")[-1]


def _markdown_to_plain(md: str) -> str:
    md = re.sub(r"^#{1,6}\s+", "\n", md, flags=re.MULTILINE)
    md = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", md)
    md = re.sub(r"`([^`]+)`", r"\1", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)
    md = re.sub(r"```[\s\S]*?```", "", md)
    md = re.sub(r"^---+$", "", md, flags=re.MULTILINE)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def post_to_naver_blog(title: str, content: str) -> str:
    if not settings.naver_id or not settings.naver_password or not settings.naver_blog_id:
        return "Naver 설정 미완료"

    blog_id = _extract_blog_id(settings.naver_blog_id)

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()

    try:
        # 로그인
        driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(2)
        driver.execute_script("document.getElementById('id').value=arguments[0]", settings.naver_id)
        driver.execute_script("document.getElementById('pw').value=arguments[0]", settings.naver_password)
        time.sleep(1)
        driver.find_element(By.ID, "log.login").click()
        print("  [Naver] 로그인 시도!")
        time.sleep(3)

        if "nidlogin" in driver.current_url or "nid.naver" in driver.current_url:
            print("  [Naver] 캡챠 뜨면 직접 풀고 Enter, 안 떴으면 그냥 Enter")
            input()

        # 글쓰기
        driver.get(f"https://blog.naver.com/{blog_id}/postwrite")
        time.sleep(7)

        try:
            driver.find_element(By.CSS_SELECTOR, ".se-help-panel-close-button").click()
            time.sleep(1)
        except Exception:
            pass

        # 제목
        pyautogui.click(781, 352)
        time.sleep(1)
        pyperclip.copy(title)
        pyautogui.hotkey("ctrl", "v")
        print("  [Naver] 제목 입력 완료!")
        time.sleep(2)

        # 본문
        pyautogui.click(516, 483)
        time.sleep(1)
        pyperclip.copy(_markdown_to_plain(content))
        pyautogui.hotkey("ctrl", "v")
        print("  [Naver] 본문 입력 완료!")
        time.sleep(2)

        # 발행
        try:
            driver.find_element(By.CSS_SELECTOR, ".publish_btn__m9KHH").click()
        except Exception:
            for btn in driver.find_elements(By.TAG_NAME, "button"):
                if "발행" in btn.text:
                    btn.click()
                    break
        time.sleep(2)

        try:
            driver.find_element(By.CSS_SELECTOR, ".confirm_btn__WEaBq").click()
        except Exception:
            for btn in driver.find_elements(By.TAG_NAME, "button"):
                if btn.text.strip() in ("발행", "확인", "공개발행"):
                    btn.click()
                    break

        time.sleep(10)
        blog_url = f"https://blog.naver.com/{blog_id}"
        driver.get(blog_url)
        time.sleep(5)
        print("  [Naver] 발행 완료!")
        time.sleep(30)
        return f"Naver 블로그 발행 완료: {blog_url}"

    except Exception as e:
        print(f"  [Naver] 오류: {e}")
        time.sleep(30)
        return f"Naver 발행 실패: {e}"
    finally:
        driver.quit()
