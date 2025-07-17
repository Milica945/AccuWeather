from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

def open_site(url='https://www.accuweather.com/'):
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(url)
    return driver

def test_search_empty_input():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')

    sleep(2)
    driver.find_element(By.CSS_SELECTOR,"input[name='query']").click()
    driver.find_element(By.CSS_SELECTOR,"input[name='query']").send_keys(Keys.ENTER)
    sleep(2)
    assert driver.find_element(By.XPATH,"/html/body/div/div[1]/div[2]/div/a[2]/h1").text=='Belgrade, Belgrade', 'Fail'
    print('When the search field is submitted empty,the current location weather is displayed.')

    close_browser(driver)

def test_search_invalid_input():

    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    sleep(2)
    driver.find_element(By.CSS_SELECTOR,"input[name='query']").click()
    driver.find_element(By.CSS_SELECTOR, "input[name='query']").send_keys('dsadasd')
    driver.find_element(By.CSS_SELECTOR,"input[name='query']").send_keys(Keys.ENTER)
    sleep(2)
    assert driver.find_element(By.XPATH,"/html/body/div/div[6]/div[1]/div[1]/div[1]").text=='No results found.', 'Fail'
    print('When an invalid location name is entered in the search field,an error message is displayed.')

    close_browser(driver)

def test_current_location_weather_box():

    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    sleep(2)
    driver.find_element(By.XPATH,"/html/body/div/div[1]/div[3]/div/div[2]/div[2]/div/a[1]").click()
    sleep(1)
    assert driver.find_element(By.XPATH,"/html/body/div/div[1]/div[2]/div/a[2]/h1").text == 'Belgrade, Belgrade', 'Fail'
    print('Weather card for the selected location is displayed.')

    close_browser(driver)

def test_menu_button_opens_sidebar_and_option_works():

    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    sleep(2)
    driver.find_element(By.CSS_SELECTOR,"svg[data-qa='navigationMenu']").click()
    sleep(1)
    driver.find_element(By.CSS_SELECTOR,"a[data-page-id='city-radar']").click()
    sleep(1)
    assert driver.find_element(By.XPATH,"//*[@id='cityRadar-container-legacy']/div[1]/div[1]/h2").text=='BELGRADE WEATHER RADAR','Fail'
    print('Menu button opens sidebar and selected option works correctly.')


def test_video_page_opening():

    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    sleep(2)
    element=driver.find_element(By.XPATH,"/html/body/div/div[6]/div[1]/div[2]/a[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",element)
    sleep(3)
    driver.find_element(By.XPATH,"/html/body/div/div[6]/div[1]/div[2]/a[5]").click()
    sleep(2)
    assert driver.find_element(By.XPATH,"/html/body/div/div[4]/div[2]/div[1]/div[3]/a[1]/h1").text=='TRENDING NOW', 'Fail'
    print('The Video button correctly navigates to the video section, displaying relevant clips.')
    close_browser(driver)

def test_newsletters_link_navigation():
    driver=open_site('https://www.accuweather.com/')
    second_tab=driver.current_window_handle
    print('Site is open.')
    sleep(2)
    driver.find_element(By.XPATH,"//*[@id='afb-nav-container']/div/ul/li[5]/a").click()
    sleep(2)
    tabs=driver.window_handles
    for tab in tabs:
        if tab !=second_tab:
            driver.switch_to.window(tab)
            break
    assert driver.current_url=='https://afb.accuweather.com/accuweatherexecutivedailynewsletters', 'Fail'
    print('The redirection to newsletters works.')
    close_browser(driver)
def test_data_suite_link_navigation():
    driver=open_site('https://www.accuweather.com/')
    second_tab=driver.current_window_handle
    print('The site is open.')
    sleep(2)
    driver.find_element(By.XPATH,"//*[@id='afb-nav-container']/div/ul/li[4]/a").click()
    sleep(2)
    tabs=driver.window_handles
    for tab in tabs:
        if tab !=second_tab:
            driver.switch_to.window(tab)
            break
    assert driver.current_url=='https://afb.accuweather.com/accuweather-data-suite-1','Fail'
    print('The redirection to data suite works.')
    close_browser(driver)


def close_browser(driver):
    driver.close()