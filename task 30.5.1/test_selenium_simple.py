
def test_search_example(selenium):
    """ Search some phrase in google and make a screenshot of the page. """

    # Open google search page:
    selenium.get('https://google.com')

    # It's better to use explicit waits instead of time.sleep
    selenium.implicitly_wait(10)  # This is a better practice than time.sleep

    # Find the field for search text input:
    search_input = selenium.find_element(By.ID, 'APjFqb')  # Используйте selenium вместо driver

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('first test')

    # Find the Search button and click it:
    search_button = selenium.find_element(By.NAME, "btnK")  # Используйте selenium и By.NAME
    search_button.click()

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')

