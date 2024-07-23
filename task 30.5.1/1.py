2
3
4
5
6
7
8
9
10
11
12
13

from selenium import webdriver

# Указываем путь к драйверу Chrome
driver = webdriver.Chrome(executable_path='D:\chromedriver-win64')

# Открываем страницу Google
driver.get("https://www.google.com")

# Проверяем, что заголовок страницы соответствует ожидаемому
assert driver.title == "Google"

# Закрываем браузер
driver.quit()