import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep

# pip install -U selenium

#run using (after running backend):
# pytest -v tests\test_selenium.py

#User Fixtures
@pytest.fixture
def user1():
    return {'username':'Student','email':'student@wsu.edu','password':'123',
    'firstname':'George', 'lastname': 'Washington', 'phone':'5093385885',
    'gpa': '4.0', 'major':'Political Science', 'graduation':'7/1776',
    'experience':'President of the United States', 'statement':'I love to apply for positions',
    'reference':'Thomas Jefferson', 'newphone':'1112223333'
    }

@pytest.fixture
def user2():
    return {'username':'Faculty','email':'faculty@wsu.edu','password':'123',
    'firstname':'John', 'lastname': 'Adams', 'phone':'1234567890'
    }    

@pytest.fixture
def registerTest():
    return {'username':'Student','email':'registerTest@wsu.edu','password':'123'}

@pytest.fixture
def emailTest():
    return {'username':'email','email':'test@gmail.com','password':'123'}

@pytest.fixture
def doubleCheck():
    return{'username':'double','email':'double@wsu.edu','password':'123'}

@pytest.fixture
def post():
    return{'title': 'President of the US', 'description':'Four year position, must be willing to work weekends',
    'time1':'12/6/2021','time2':'12/6/2025', 'time':'80','requirements':'Experience in politics'
    }

#https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/

#Setting up browser

@pytest.fixture
def browser():
    CHROME_PATH = 'c:\\Webdriver' #Add a new folder called Webdriver
    print(CHROME_PATH)
    opts = Options()
    opts.headless = False #Change to true  if you don't want it to open browser
    driver = webdriver.Chrome(options=opts, executable_path= CHROME_PATH + '/chromedriver.exe') #Add chromedriver to Webdriver folder
    driver.implicitly_wait(10)

    yield driver
    
    driver.quit()


#Tests
#1. Testing for selecting both student and faculty usertypes
def test_double_select(browser,doubleCheck):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(doubleCheck['username'])
    browser.find_element_by_name("email").send_keys(doubleCheck['email'])
    browser.find_element_by_name("faculty").click()
    browser.find_element_by_name("student").click()
    browser.find_element_by_name("password").send_keys(doubleCheck['password'])
    browser.find_element_by_name("password2").send_keys(doubleCheck['password'])
    browser.find_element_by_name("submit").click()

    content = browser.page_source
    assert 'Please select student OR faculty.' in content

#2. Test for registering a faculty member
def test_faculty_register(browser,user2):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("email").send_keys(user2['email'])
    browser.find_element_by_name("faculty").click()
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("password2").send_keys(user2['password'])
    browser.find_element_by_name("submit").click()

    content = browser.page_source
    assert 'Registration Successful.' in content

#3. Testing for registering as a student
def test_register(browser,user1):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(user1['username'])
    browser.find_element_by_name("email").send_keys(user1['email'])
    browser.find_element_by_name("student").click()
    browser.find_element_by_name("password").send_keys(user1['password'])
    browser.find_element_by_name("password2").send_keys(user1['password'])
    browser.find_element_by_name("submit").click()

    browser.find_element_by_name("firstname").send_keys(user1['firstname'])
    browser.find_element_by_name("lastname").send_keys(user1['lastname'])
    browser.find_element_by_name("phone").send_keys(user1['phone'])
    browser.find_element_by_name("gpa").send_keys(user1['gpa'])
    browser.find_element_by_name("major").send_keys(user1['major'])
    browser.find_element_by_name("graduation").send_keys(user1['graduation'])

    browser.find_element_by_id("research-0").click()
    browser.find_element_by_id("research-1").click()
    browser.find_element_by_id("research-2").click()

    browser.find_element_by_id("language-2").click()
    browser.find_element_by_id("language-3").click()
    browser.find_element_by_id("language-4").click()

    browser.find_element_by_name("experience").send_keys(user1['experience'])

    browser.find_element_by_name("submit").click()

    content = browser.page_source
    assert 'Your account has been updated' in content

#4. Testing for validation error for duplicate username
def test_register_fail_user(browser, registerTest):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(registerTest['username'])
    browser.find_element_by_name("email").send_keys(registerTest['email'])
    browser.find_element_by_name("student").click()
    browser.find_element_by_name("password").send_keys(registerTest['password'])
    browser.find_element_by_name("password2").send_keys(registerTest['password'])
    browser.find_element_by_name("submit").click()

    content = browser.page_source

    assert 'This username already exists. Please use a different username.' in content

#5. Testing for WSU email domain
def test_email_domain(browser, emailTest):
    browser.get('http://localhost:5000/register')

    browser.find_element_by_name("username").send_keys(emailTest['username'])
    browser.find_element_by_name("email").send_keys(emailTest['email'])
    browser.find_element_by_name("student").click()
    browser.find_element_by_name("password").send_keys(emailTest['password'])
    browser.find_element_by_name("password2").send_keys(emailTest['password'])
    browser.find_element_by_name("submit").click()

    content = browser.page_source

    assert 'Please register using a wsu.edu email address' in content

#6. Testing for creating a position without first adding additional information
def test_post_no_info(browser, user2):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')

    content = browser.page_source
    assert 'Please finish setting up your profile before creating a position' in content

#7. Testing for creating a position after setting up profile
def test_post(browser, user2,post):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user2['username'])
    browser.find_element_by_name("password").send_keys(user2['password'])
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')
    browser.find_element_by_name("firstname").send_keys(user2['firstname'])
    browser.find_element_by_name("lastname").send_keys(user2['lastname'])
    browser.find_element_by_name("phone").send_keys(user2['phone'])
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/post')
    browser.find_element_by_name("project_title").send_keys(post['title'])
    browser.find_element_by_name("description").send_keys(post['description'])
    browser.find_element_by_name("date1").send_keys(post['time1'])
    browser.find_element_by_name("date2").send_keys(post['time2'])
    browser.find_element_by_name("time").send_keys(post['time'])
    browser.find_element_by_name("requirements").send_keys(post['requirements'])

    browser.find_element_by_id("research-1").click()
    browser.find_element_by_id("research-3").click()

    browser.find_element_by_id("language-2").click()
    browser.find_element_by_id("language-4").click()

    browser.find_element_by_name("submit").click()

    content = browser.page_source
    assert 'Research position President of the US has been posted' in content
 
 #8. Testing for applying to a position
def test_apply(browser, user1):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user1['username'])
    browser.find_element_by_name("password").send_keys(user1['password'])
    browser.find_element_by_name("submit").click()

    browser.find_element_by_id("apply").click()
    browser.find_element_by_name("statement").send_keys(user1['statement'])
    browser.find_element_by_name("reference").send_keys(user1['reference'])
    browser.find_element_by_name("apply").click()

    content = browser.page_source

    assert'You applied to President of the US!' in content

#9. Testing for withdrawing an application
def test_withdraw(browser, user1):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user1['username'])
    browser.find_element_by_name("password").send_keys(user1['password'])
    browser.find_element_by_name("submit").click()

    browser.find_element_by_id("withdraw").click()

    content = browser.page_source
    assert 'You have successfully withdrawed from President of the US!' in content

#10. Testing for viewing applications without applying to any
def test_no_apps(browser,user1):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user1['username'])
    browser.find_element_by_name("password").send_keys(user1['password'])
    browser.find_element_by_name("submit").click()

    browser.get('http://localhost:5000/submittedapps')

    content = browser.page_source
    assert 'You have not submitted any applications!' in content

#11. Testing for editing profile information
def test_edit_profile(browser, user1):
    browser.get('http://localhost:5000/login')

    browser.find_element_by_name("username").send_keys(user1['username'])
    browser.find_element_by_name("password").send_keys(user1['password'])
    browser.find_element_by_name("submit").click()
    
    browser.get('http://localhost:5000/edit')
    browser.find_element_by_name("phone").clear()
    browser.find_element_by_name("phone").send_keys(user1['newphone'])

    browser.find_element_by_name("submit").click()

    content = browser.page_source
    assert 'Your account has been updated' in content

#TODO:
# Delete position
# Restricted routes
# Restricted login pages
