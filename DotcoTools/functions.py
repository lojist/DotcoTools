from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import requests
import time

def login(username, password, browser):
    """Open a browser with selenium and login with given username and password."""

    # go to site
    browser.get('https://incels.co')

    # log in
    browser.find_element_by_xpath("//span[text()='Log in']/..").click()
    time.sleep(2)
    login_input = browser.find_element_by_name('login')
    password_input = browser.find_element_by_name('password')

    login_input.send_keys(username)
    password_input.send_keys(password)
    browser.find_element_by_css_selector(
        'button[class="button--primary button button--icon button--icon--login"]').click()

def get_usernames(start=1, end=257):
    """Pulls usernames from the members list page-by-page (a start and end page can be entered, by default it gets all)
        and returns them as a list. Does not require login."""

    usernames_list = []
    for i in range(start, end):
        print(f'Page {i - 1} out of {end} complete...')

        r = requests.get(f'https://incels.co/members/list?page={i}')
        page = r.content
        soup = BeautifulSoup(page, 'lxml')

        names_unsorted = soup.find_all('div', class_='contentRow-main')

        for name_chunk in names_unsorted:
            try:
                username = name_chunk.select('span[class*="username--style"]')[0].text
                usernames_list.append(username)
            except:
                raise Exception('Error with the get_usernames function (it\'s probably the css selector.)')

    return usernames_list

def time_online_sanitizer(time_online_raw_string):
    """Takes times in the format of strings formatted as 'hours:minutes' and converts them to a float of hours with
        decimals for fractions of hours"""

    time_online_hours = ''
    time_online_minutes = ''
    colon_reached = False

    for character in time_online_raw_string:
        if not colon_reached:
            if character != ':':
                time_online_hours += character
            else:
                colon_reached = True
        else:
            time_online_minutes += character

        if not time_online_minutes:
            time_online_minutes = 0

    return float(time_online_hours) + float(int(time_online_minutes) / 60)

def ignore_user(ID, browser):
    """Ignores a user by ID number, also requires selenium webdriver. Requires login."""

    browser.get(f'https://incels.co/members/{ID}/ignore')
    ignore_button = browser.find_element_by_xpath('//span[contains(text(), "Ignore")]')
    ignore_button.click()

def unignore_all(browser):
    """Unignores every user on ignore list. Requires login."""
    browser.get('https://incels.co/account/ignored')
    unignore_buttons = browser.find_elements_by_xpath("//ol/li/div/div/div/a[contains(@data-sk-unignore, 'Unignore')]")

    for button in unignore_buttons:
        button.click()

def get_id_username(browser, ID):
    """Gets the username of a certain ID, returns none if there is no username attached to the ID. Requires log in."""
    user_url = f'https://incels.co/members/{ID}'
    browser.get(user_url)

    if browser.current_url != user_url:
        title = browser.find_element_by_css_selector('title')
        title_text = title.get_attribute('textContent')
        name = ''

        for character in title_text:
            if character != '|':
                name += character
            else:
                name.strip()
                break

        if ') ' in name:
            end_parenthesis_reached = False
            for character in name:
                if not end_parenthesis_reached:
                    if character == ')':
                        end_parenthesis_reached = True
                        name = ''
                    continue
                else:
                    name += character

        return {'username': name.strip(), 'ID': ID}

    else:
        return None

def get_id_postcount(browser, ID):
    """Gets the postcount of a certain ID, returns none if there is no username attached to the ID. Requires log in."""

    browser.get(f'https://incels.co/members/{ID}')
    if browser.current_url != f'https://incels.co/members/{ID}':
        postcount_string = browser.find_element_by_xpath('//dd/a').text
        postcount_int = int(postcount_string.replace(',', ''))
        return postcount_int
    else:
        return None

def get_id_join_date(browser, ID):
    """Gets the join date of a certain ID, returns none if there is no username attached to the ID. Requires log in."""

    browser.get(f'https://incels.co/members/{ID}')
    if browser.current_url != f'https://incels.co/members/{ID}':
        time_selector = browser.find_element_by_css_selector('time')
        join_date = time_selector.get_attribute('data-time')
        return join_date
    else:
        return None

def post(thread_url, message, browser):
    """Takes a thread url and a message and posts the message to that url. Requires login."""

    browser.get(thread_url)
    message_box = browser.find_element_by_xpath('//div[contains(@class, "fr-element")]')
    message_box.send_keys(message)
    message_box.send_keys(Keys.TAB)
    message_box.send_keys(Keys.ENTER)
    browser.find_element_by_xpath('//*[text()[contains(., "Post reply")]]').click()

def get_thread_last_reply_user(thread_url, browser):
    """Returns the username of the last user to reply to a given thread and page. Requires login."""
    browser.get(thread_url)
    messages = browser.find_elements_by_xpath('//article[contains(@class, "message")]')
    last_message = messages[-2]

    return last_message.get_attribute('data-author')
