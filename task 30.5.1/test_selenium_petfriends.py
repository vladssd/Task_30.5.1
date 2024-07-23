import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("web_browser")
def test_petfriends(web_browser):
    # Open PetFriends base page:
    web_browser.get("https://petfriends.skillfactory.ru/")

    # Ожидание загрузки кнопки нового пользователя
    btn_newuser = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]"))
    )
    btn_newuser.click()

    # Ожидание загрузки кнопки существующего пользователя
    btn_exist_acc = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "У меня уже есть аккаунт"))
    )
    btn_exist_acc.click()

    # Ожидание поля ввода email
    field_email = WebDriverWait(web_browser, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    field_email.clear()
    field_email.send_keys("12314@1231.ru")  # Используем сохраненный email

    # Ожидание поля ввода пароля
    field_pass = WebDriverWait(web_browser, 10).until(
        EC.visibility_of_element_located((By.ID, "pass"))
    )
    field_pass.clear()
    field_pass.send_keys("123123")  # Используем сохраненный пароль

    # Ожидание кнопки отправки формы
    btn_submit = WebDriverWait(web_browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    btn_submit.click()

    # Проверяем, что мы находимся на нужной странице
    assert web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets', "login error"
