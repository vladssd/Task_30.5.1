import pytest
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Фикстура для настройки опций Firefox
@pytest.fixture
def firefox_options():
    options = FirefoxOptions()
    options.binary = '/path/to/firefox-bin'  # Путь к исполняемому файлу Firefox
    options.add_argument('-foreground')  # Запуск Firefox на переднем плане
    options.set_preference('browser.anchor_color', '#FF0000')  # Цвет якоря браузера
    return options

# Фикстура для настройки опций Chrome
@pytest.fixture
def chrome_options():
    options = ChromeOptions()
    options.binary_location = r'C:\Program Files\Google\Chrome\Application'  # Местоположение Chrome
    # options.add_extension('/path/to/extension.crx')  # Добавление расширения
    options.add_argument('--kiosk')  # Запуск Chrome в режиме киоска
    return options

# Хук для создания отчёта о результатах теста
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# Функция для получения строки документации тестового случая
def get_test_case_docstring(item):
    full_name = ''
    if item._obj.__doc__:
        name = ' '.join(str(item._obj.__doc__.split('.')[0]).strip().split())
        full_name = name
        if hasattr(item, 'callspec'):
            params = item.callspec.params
            res_keys = sorted(params)
            res = ['{0}_"{1}"'.format(k, params[k]) for k in res_keys]
            full_name += ' Параметры ' + ', '.join(res).replace(':', '')
    return full_name

# Хук для изменения имени тестового случая
@pytest.hookimpl(tryfirst=True)
def pytest_itemcollected(item):
    if item._obj.__doc__:
        item._nodeid = get_test_case_docstring(item)

# Хук для изменения имени тестового случая при использовании --collect-only
@pytest.hookimpl(tryfirst=True)
def pytest_collection_finish(session):
    if session.config.option.collectonly is True:
        for item in session.items:
            if item._obj.__doc__:
                full_name = get_test_case_docstring(item)
                print(full_name)
        pytest.exit('Готово!')

# Фикстура для инициализации браузера
@pytest.fixture
def web_browser(request):
    driver_path = r'D:\chromedriver-win64'
    browser = webdriver.Chrome(executable_path=driver_path, options=request.getfixturevalue('chrome_options'))
    yield browser
    # Закрытие браузера после выполнения теста
    browser.quit()
    # browser = webdriver.Chrome(options=request.getfixturevalue('chrome_options'))
    # browser.set_window_size(1400, 1000)
    # yield browser
    if request.node.rep_call.failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)
        except Exception as e:
            print(f'Произошла ошибка при попытке сохранения скриншота: {e}')
