import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Chrome options for faster page loading such as disable images
def loadChromeOptions():
    options = Options()
    options.add_argument("user-data-dir=ChromeData/dunk")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-3d-apis")
    options.add_argument("--disable-modal-animations")
    options.add_argument("--disable-login-animations")
    options.add_argument("--disable-threaded-animation")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-component-extensions-with-background-pages")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-font-subpixel-positioning")
    options.add_argument("--disable-highres-timer")
    options.add_argument("--disable-lcd-text")
    options.add_argument("--disable-multi-display-layout")
    options.add_argument("--disable-overscroll-edge-effect")
    options.add_argument("--disable-pepper-3d")
    options.add_argument("--disable-smooth-scrolling")
    options.add_argument("--disable-system-font-check")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    return options

browser = webdriver.Chrome(desired_capabilities={"pageLoadStrategy": "none"}, options=loadChromeOptions())
wait = WebDriverWait(browser, 120)

def purchase(url, size, last_digits):
    browser.get(url)

    select_size = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tamanho__id%s"]' %str(size))))
    browser.execute_script("arguments[0].click()", select_size)

    cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-comprar"]')))
    browser.execute_script("arguments[0].click()", cart_button)

    wait.until(EC.url_contains("Carrinho"))
    browser.get("https://www.nike.com.br/Checkout")

    address = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seguir-pagamento"]')))
    time.sleep(0.25)
    address = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="seguir-pagamento"]')))
    browser.execute_script("arguments[0].click()", address)

    browser.switch_to_active_element
    confirm_address = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".button.undefined")))
    browser.execute_script("arguments[0].click()", confirm_address[0])

    card1 = browser.find_element_by_xpath('//*[@id="cartoes-salvos"]')
    card2 = browser.find_element_by_xpath('//*[@id="cartoes-salvos"]/ul')
    browser.execute_script("arguments[0].setAttribute('class','select-cta active')", card1)
    browser.execute_script("arguments[0].setAttribute('style','display: block;')", card2)

    credit_card = browser.find_element_by_css_selector("input[data-lastdigits='%s']" %str(last_digits))
    browser.execute_script("arguments[0].click()", credit_card)

    payment_menu = browser.find_element_by_xpath('//*[@id="saved-card-installments"]')
    browser.execute_script("arguments[0].click()", payment_menu)

    payment = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="saved-card-installments"]')))
    browser.execute_script("arguments[0].selectedIndex = 9;", payment)

    accept_terms = browser.find_element_by_xpath('//*[@id="politica-trocas"]')
    browser.execute_script("arguments[0].click()", accept_terms)

    confirm_purchase = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirmar-pagamento"]')))
    browser.execute_script("arguments[0].click()", confirm_purchase)


if __name__ == '__main__':
    url = "www.productpage.com.br" # shoe url
    size = 40 # shoe size
    cc_last_digits = 1234  # last digits of registered credit card for locating webelement in page
    purchase(url, size, cc_last_digits) # automated purchase
