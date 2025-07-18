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

def test_data_suite_product_services_redirect():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    driver.find_element(By.XPATH, "//*[@id='afb-nav-container']/div/ul/li[4]/a").click()
    sleep(2)
    print('Clicked on the "Data Suite" link.')
    original_tab = driver.current_window_handle
    for tab in driver.window_handles:
        if tab != original_tab:
            driver.switch_to.window(tab)
            break
    print('Switched to the "Data Suite" tab.')
    driver.find_element(By.XPATH,"//*[@id='hs_cos_wrapper_navigation-primary']/ul/li[1]/a").click()
    sleep(2)
    print('Clicked on the "Products & Services" link.')
    assert driver.find_element(By.XPATH,"//*[@id='hs_cos_wrapper_module_166481382230911']/ul/li[2]/span").text=='PRODUCTS & SERVICES','Fail'
    print('Redirection to "Products & Services" page successful.')
    close_browser(driver)

def test_dropdown_option_change_to_videos():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    driver.find_element(By.XPATH,"/html/body/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[1]").click()
    sleep(1)
    print('Dropdown menu opened.')
    driver.find_element(By.XPATH,"/html/body/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[2]/a[3]/span").click()
    sleep(2)
    print('"Videos" option selected from dropdown.')
    assert driver.find_element(By.XPATH,"/html/body/div/div[1]/div[3]/div/div[1]/div[1]/div/div/div[1]/span").text=='Videos', 'Fail'
    print('Dropdown successfully switched to "Videos" and is functioning as expected.')
    close_browser(driver)

def test_forensics_button_redirects_to_correct_url():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    driver.find_element(By.XPATH,"//*[@id='afb-nav-container']/div/ul/li[5]/a").click()
    sleep(2)
    print('Clicked on "Forensics" button.')
    second_tab = driver.current_window_handle
    tabs = driver.window_handles
    for tab in tabs:
        if tab != second_tab:
            driver.switch_to.window(tab)
            break
    sleep(1)
    assert driver.current_url== 'https://afb.accuweather.com/accuweather-forensicservices','Fail'
    print('"Forensics" page opened successfully.')
    close_browser(driver)

def test_contact_us_functionality():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    element= driver.find_element(By.XPATH,"/html/body/div/div[10]/span/div/div[2]/div[1]/div[1]/div[2]/a[6]")
    print('Found "Contact Us" link.')
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});",element)
    sleep(2)
    print('Scrolled to "Contact Us" link.')
    driver.find_element(By.XPATH,"/html/body/div/div[10]/span/div/div[2]/div[1]/div[1]/div[2]/a[6]").click()
    sleep(2)
    second_tab= driver.current_window_handle
    tabs = driver.window_handles
    for tab in tabs:
        if tab != second_tab:
            driver.switch_to.window(tab)
            break
    print('Switched to "Contact Us" tab.')
    sleep(1)
    assert driver.current_url=='https://www.accuweather.com/en/contact', 'Fail'
    print('Redirection to "Contact Us" page works correctly.')
    close_browser(driver)

def test_accuweather_api_reference_access():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    element=driver.find_element(By.XPATH,"/html/body/div/div[10]/span/div/div[2]/div[2]/div/div[2]/a[4]")
    driver.execute_script("arguments[0].scrollIntoView({block : 'center'});",element)
    sleep(2)
    print('Scrolled on "API Reference" link.')
    driver.find_element(By.XPATH,"/html/body/div/div[10]/span/div/div[2]/div[2]/div/div[2]/a[4]").click()
    sleep(2)
    print('Clicked on "API Reference link."')
    original_tab=driver.current_window_handle
    for tab in driver.window_handles:
        if tab != original_tab:
            driver.switch_to.window(tab)
            break
    print('Switched to "API Reference" tab.')
    driver.find_element(By.XPATH,"//*[@id='navbar']/div/div/div/nav/ul[1]/li[1]/a").click()
    sleep(2)
    print('Clicked on first navigation link inside "API Reference" page.')
    assert driver.find_element(By.XPATH,"/html/body/div[4]/section/div/div/div/h1").text== 'API Reference','Fail'
    print('Redirection to API reference works correctly.')
    close_browser(driver)

def test_air_quality_link_functionality():
    driver=open_site('https://www.accuweather.com/')
    print('Site is open.')
    driver.find_element(By.CSS_SELECTOR,"a[data-location-key='298198']").click()
    sleep(2)
    print('Clicked on location link.')
    driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[3]/a[7]/span").click()
    sleep(2)
    print('Clicked on "Air Quality" button.')
    assert driver.find_element(By.XPATH,"//*[@id='current']/div/h2").text=='CURRENT AIR QUALITY','Fail'
    print('"Air Quality" page is displayed correctly.')
    close_browser(driver)

def close_browser(driver):
    driver.close()