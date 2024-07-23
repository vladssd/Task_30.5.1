from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle


def test_petfriends(selenium):
    """ Search some phrase in google and make a screenshot of the page. """

    # Open PetFriends base page:
    selenium.get("https://petfriends1.herokuapp.com/")

    # Use explicit waits instead of time.sleep
    wait = WebDriverWait(selenium, 10)

    # Find the button for new user registration and click it:
    btn_newuser = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick=\"/new_user\"]")))
    btn_newuser.click()

    # Find the link for existing users and click it:
    btn_exist_acc = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "У меня уже есть аккаунт")))
    btn_exist_acc.click()

    # Find the email field and fill it in:
    field_email = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    field_email.clear()
    field_email.send_keys("134.x@gmail.com")

    # Find the password field and fill it in:
    field_pass = wait.until(EC.visibility_of_element_located((By.ID, "pass")))
    field_pass.clear()
    field_pass.send_keys("qwerty12341231")

    # Find the submit button and click it:
    btn_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    btn_submit.click()

    # Save cookies of the browser after the login
    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(selenium.get_cookies(), cookies)

    # Make the screenshot of browser window:
    selenium.save_screenshot('result_petfriends.png')
