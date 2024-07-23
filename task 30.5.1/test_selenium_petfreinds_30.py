import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Фикстура для инициализации драйвера
@pytest.fixture(autouse=True)
def driver_setup():
    web_driver = webdriver.Chrome(ChromeDriverManager().install())
    web_driver.implicitly_wait(10)  # Установка неявного ожидания для всех элементов
    web_driver.get('https://petfriends.skillfactory.ru/login')
    yield web_driver
    web_driver.quit()

# Тест для проверки требований к списку питомцев
def test_pets_list_requirements(driver_setup):
    # Явные ожидания для элементов страницы
    WebDriverWait(driver_setup, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    driver_setup.find_element(By.ID, 'email').send_keys('12314@1231.ru')
    driver_setup.find_element(By.ID, 'pass').send_keys('123123')
    driver_setup.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    WebDriverWait(driver_setup, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.card-deck .card-img-top'))
    )

    # Получаем элементы с изображениями, именами и описаниями питомцев
    images = driver_setup.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver_setup.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver_setup.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Проверяем, что присутствуют все питомцы
    assert len(names) == len(descriptions) == len(images)

    # Проверяем, что хотя бы у половины питомцев есть фото
    photos_present = sum(1 for image in images if image.get_attribute('src') != '')
    assert photos_present >= len(images) / 2

    # Проверяем, что у всех питомцев есть имя, возраст и порода
    for description in descriptions:
        assert ', ' in description.text
        parts = description.text.split(", ")
        assert len(parts) == 3

    # Проверяем, что у всех питомцев разные имена
    unique_names = set([name.text for name in names])
    assert len(unique_names) == len(names)

    # Проверяем, что в списке нет повторяющихся питомцев
    unique_pets = set()
    for i in range(len(names)):
        pet_info = (names[i].text, descriptions[i].text)
        assert pet_info not in unique_pets
        unique_pets.add(pet_info)

