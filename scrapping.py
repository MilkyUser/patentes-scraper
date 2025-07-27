from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Generator


_INPI_URL = 'https://busca.inpi.gov.br/pePI/jsp/patentes/PatenteSearchBasico.jsp'


def setup_driver() -> tuple[webdriver.Chrome, WebDriverWait]:
    
    options = Options()
    #options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-notifications')
    options.add_experimental_option(
        "prefs", {
            "profile.managed_default_content_settings.images": 2  # Bloqueia download de imagens
        }
    )
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(
        driver,
        timeout=12,
        poll_frequency=0.3,
        ignored_exceptions=(NoSuchElementException)
    )
    return driver, wait


def navigate_to_search_page(driver, wait):
    
    try:
        driver.get(_INPI_URL)
        botao_continuar = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".marcador a:nth-of-type(1)"))
        )
        botao_continuar.click()
        wait.until(EC.number_of_windows_to_be(2))
        window_handles = driver.window_handles
        driver.close()
        driver.switch_to.window(window_handles[-1])
        botao_patentes = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#Map3 area:nth-child(5)"))
        )
        driver.execute_script("arguments[0].click();", botao_patentes)
        driver.implicitly_wait(1)
    except Exception as e:
        driver.save_screenshot("debug-screenshots/navigation_error.png")
        raise RuntimeError(f"Navigation failed: {str(e)}") from e


def search_by_id(wait, search_key) -> str:

    try:
        search_field = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input.basic[name="NumPedido"]'))
        )
        search_field.clear()
        search_field.send_keys(search_key)
        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input.basic:nth-child(2)'))
        )
        search_button.click()
        result_link = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a.visitado'))
        )
        result_link.click()
        data = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#principal > table:nth-child(6)'))
        ).get_attribute('innerHTML')
        back_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'a[href="../jsp/patentes/PatenteSearchBasico.jsp"]')))
        back_button.click()
        return data
        
    except Exception as e:
        raise RuntimeError(f"Search failed for {search_key}: {str(e)}") from e


def batch_search(driver, wait, search_ids) -> Generator[dict[str, str | None]]:
    
    for sid in search_ids:

        try:
            yield {'doc-number': sid, 'data': search_by_id(wait, sid)}
        
        except RuntimeError as re:

            if isinstance(re.__cause__, TimeoutException):
                navigate_to_search_page(driver, wait)
                yield {'doc-number': sid, 'data': None}
                
            else:
                raise
