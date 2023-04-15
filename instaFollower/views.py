from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# models
from .models import Account


# Selenium function
def follow_info(username,password):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    

    import time

    USERNAME = username
    PASSWORD = password

    
    # Start driver
    
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)


    
    # driver.maximize_window()  
    driver.get('https://www.instagram.com/accounts/login/')

    # Enter username and password
    time.sleep(10)
    username_input = driver.find_element(By.NAME,'username')
    username_input.send_keys(USERNAME)
    password_input = driver.find_element(By.NAME,'password')
    password_input.send_keys(PASSWORD)
    print('username entered')


    # Click login button
    time.sleep(2)
    login_button = driver.find_element(By.XPATH,"//button[@type='submit']")
    login_button.click()

    # Get Profile page
    time.sleep(10)
    profile_button = driver.find_element(By.XPATH,"//div[text()='Profile']")
    profile_button.click()

    # _ac8f

    # Get follow data
    time.sleep(10)
    followers_s = driver.find_elements(By.CLASS_NAME,'_ac2a')[1].text

    following_s = driver.find_elements(By.CLASS_NAME,'_ac2a')[2].text

    # Get username
    user_name = driver.find_element(By.TAG_NAME,"h2").text

    # Quit browser
    driver.quit()

    # Save data
    data = Account(login=USERNAME,password=PASSWORD,username=user_name,followers=followers_s,following=following_s)
    data.save()

# Create your views here.
def home(request):
    accounts = Account.objects.all()
    return render(request, "home.html",{"accounts":accounts})


def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        # Validator
        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(
                    request, "sign-up.html", {"error": "Username already exists!"}
                )
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect("login")

    return render(request, "sign-up.html")


def log_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "login.html", {"error": "Username or password is wrong!"}
            )

    return render(request, "login.html")


def log_out(request):
    logout(request)
    return redirect("home")


def add(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        follow_info(username,password)
        
        return redirect("home")
    
    return render(request, "form.html")
