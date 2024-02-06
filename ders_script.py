import traceback

try:
    from selenium import webdriver
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.common.by import By
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions
    import re
    import time

### BURADAN YUKARISINA DOKUNMA

    start_prompt = False #FALSE OLUNCA PENCERE AÇILIR AÇILMAZ İŞLEMLERİ YAPAR
    page_prompt = True #FALSE OLUNCA OTURUM AÇIP SAYFA YENİLEDİKTEN SONRA DERS SEÇİM SAYFASINA GİRMEYE ÇALIŞIR
    select_prompt = False #FALSE OLUNCA "Eklemek için Enter'a bas" UYARISI VERMEDEN DERSİ EKLEMEYE ÇALIŞIR

    course1 = {"active": True, "abb": "PSY", "code": "101", "sec": "01", "rpt": True, "rpt_w": "POLS101"} #SECTION SEÇİMİNDE TEK HANELİLERDE BAŞA 0 KOY
    course2 = {"active": True, "abb": "HTR", "code": "312", "sec": "34", "rpt": True, "rpt_w": ""} #AYNI DERSLE TEKRARSA rpt_w DOLDURMA
    course3 = {"active": True, "abb": "ATA", "code": "507", "sec": "01", "rpt": False, "rpt_w": ""}
    course4 = {"active": False, "abb": "", "code": "", "sec": "", "rpt": False, "rpt_w": ""}
    course5 = {"active": False, "abb": "ATA", "code": "571", "sec": "08", "rpt": False, "rpt_w": ""}
    course6 = {"active": False, "abb": "", "code": "", "sec": "", "rpt": False, "rpt_w": ""}
    course7 = {"active": False, "abb": "MATH", "code": "101", "sec": "02", "rpt": False, "rpt_w": ""}

    student_id = "" #öğrenci no
    pwd = "" #öbikas şifresi

### BURADAN AŞAĞISINA DOKUNMA

    courses = (course1, course2, course3, course4, course5, course6, course7)

    ac_check = False #BUNLARA DOKUNMA
    rpt_opts = []

    for i in courses:
        if i["active"]:
            ac_check = True

    if not ac_check:
        input("Hiçbir ders aktifleştirilmemiş.")
        exit()

    def repeat_options(select_obj):
        for i in select_obj:
            rpt_opts.append(i.text)

    def rpt_check(course_abb, course_cd, rpt_w=""):
        if rpt_w != "":
            match = re.match(r"([a-z]+)([0-9]+)", rpt_w.lower(), re.I)
            if match:
                course_abb, course_cd = match.groups()
        for i in rpt_opts:
            if (course_abb.upper() + course_cd in i.upper()) or (course_abb.upper() + " " + course_cd in i.upper()):
                return i
        print(f"Uyarı: {course_abb.upper()}{course_cd} için repeat seçeneği yok!")
        return rpt_opts[0]


    ########## XPATHS ##########

    iframe_x = '//*[@id="ifCPL"]'

    nm_box = '//*[@id="txtUsername"]' #login sayfası okul no
    pw_box = '//*[@id="txtPassword"]' # login sayfası şifre
    lg_btn = '//*[@id="btnLogin"]' # login sayfası login tuşu

    crs_sl_btn = '/html/body/form/div[3]/div[3]/div[4]/div[1]/div/div/ul/li[4]/a'

    add_button = "/html/body/form/div/center/form/center[1]/table/tbody/tr[10]/td/input" #quick add tuşu

    c1_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[3]/td[1]/input" #1. ders harf kodu
    c1_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[3]/td[2]/input" #1. ders sayı kodu
    c1_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[3]/td[3]/select" #1. ders section kodu
    c1_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[3]/td[5]/select" #1. ders repeat kutusu

    c2_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[4]/td[1]/input"
    c2_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[4]/td[2]/input"
    c2_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[4]/td[3]/select"
    c2_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[4]/td[5]/select"

    c3_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[5]/td[1]/input"
    c3_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[5]/td[2]/input"
    c3_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[5]/td[3]/select"
    c3_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[5]/td[5]/select"

    c4_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[6]/td[1]/input"
    c4_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[6]/td[2]/input"
    c4_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[6]/td[3]/select"
    c4_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[6]/td[5]/select"

    c5_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[7]/td[1]/input"
    c5_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[7]/td[2]/input"
    c5_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[7]/td[3]/select"
    c5_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[7]/td[5]/select"

    c6_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[8]/td[1]/input"
    c6_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[8]/td[2]/input"
    c6_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[8]/td[3]/select"
    c6_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[8]/td[5]/select"

    c7_abb = "/html/body/form/div/center/form/center[1]/table/tbody/tr[9]/td[1]/input"
    c7_code = "/html/body/form/div/center/form/center[1]/table/tbody/tr[9]/td[2]/input"
    c7_sec = "/html/body/form/div/center/form/center[1]/table/tbody/tr[9]/td[3]/select"
    c7_rpt = "/html/body/form/div/center/form/center[1]/table/tbody/tr[9]/td[5]/select"


    #############################


    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    driver.get("https://registration.boun.edu.tr/")

    if start_prompt:
        input("Başlamak için Enter'a basın.")

    driver.find_element(by=By.XPATH, value=nm_box).send_keys(student_id)
    driver.find_element(by=By.XPATH, value=pw_box).send_keys(pwd)
    driver.find_element(by=By.XPATH, value=lg_btn).click()

    driver.refresh()

    if page_prompt:
        input("Devam etmek için Enter'a basın.")

    driver.find_element(by=By.XPATH, value=crs_sl_btn).click()

    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, iframe_x)))

    iframe = driver.find_element(by=By.XPATH, value=iframe_x)

    driver.switch_to.frame(iframe)

    WebDriverWait(driver, 300).until(expected_conditions.presence_of_element_located((By.XPATH, add_button)))

    repeat_options(Select(driver.find_element(by=By.XPATH, value=c1_rpt)).options)

    if select_prompt:
        input("Eklemek için Enter'a basın.")

    if driver.current_url != "https://registration.boun.edu.tr/buis/manage/ObikasASPFrame.aspx?url=/scripts/loginst.asp":
        print("Ders seçimi sayfasında olmayabilirsin.")

    if course1["active"]:
        driver.find_element(by=By.XPATH, value=c1_abb).send_keys(course1["abb"])
        driver.find_element(by=By.XPATH, value=c1_code).send_keys(course1["code"])
        c1_dropdown = Select(driver.find_element(by=By.XPATH, value=c1_sec))
        c1_dropdown.select_by_value(course1["sec"])
        if course1["rpt"]:
            c1r_dropdown = Select(driver.find_element(by=By.XPATH, value=c1_rpt))
            c1r_dropdown.select_by_visible_text(rpt_check(course1["abb"], course1["code"], course1["rpt_w"]))

    if course2["active"]:
        driver.find_element(by=By.XPATH, value=c2_abb).send_keys(course2["abb"])
        driver.find_element(by=By.XPATH, value=c2_code).send_keys(course2["code"])
        c2_dropdown = Select(driver.find_element(by=By.XPATH, value=c2_sec))
        c2_dropdown.select_by_value(course2["sec"])
        if course2["rpt"]:
            c2r_dropdown = Select(driver.find_element(by=By.XPATH, value=c2_rpt))
            c2r_dropdown.select_by_visible_text(rpt_check(course2["abb"], course2["code"], course2["rpt_w"]))

    if course3["active"]:
        driver.find_element(by=By.XPATH, value=c3_abb).send_keys(course3["abb"])
        driver.find_element(by=By.XPATH, value=c3_code).send_keys(course3["code"])
        c3_dropdown = Select(driver.find_element(by=By.XPATH, value=c3_sec))
        c3_dropdown.select_by_value(course3["sec"])
        if course3["rpt"]:
            c3r_dropdown = Select(driver.find_element(by=By.XPATH, value=c3_rpt))
            c3r_dropdown.select_by_visible_text(rpt_check(course1["abb"], course3["code"], course3["rpt_w"]))

    if course4["active"]:
        driver.find_element(by=By.XPATH, value=c4_abb).send_keys(course4["abb"])
        driver.find_element(by=By.XPATH, value=c4_code).send_keys(course4["code"])
        c4_dropdown = Select(driver.find_element(by=By.XPATH, value=c4_sec))
        c4_dropdown.select_by_value(course4["sec"])
        if course4["rpt"]:
            c4r_dropdown = Select(driver.find_element(by=By.XPATH, value=c4_rpt))
            c4r_dropdown.select_by_visible_text(rpt_check(course4["abb"], course4["code"], course4["rpt_w"]))

    if course5["active"]:
        driver.find_element(by=By.XPATH, value=c5_abb).send_keys(course5["abb"])
        driver.find_element(by=By.XPATH, value=c5_code).send_keys(course5["code"])
        c5_dropdown = Select(driver.find_element(by=By.XPATH, value=c5_sec))
        c5_dropdown.select_by_value(course5["sec"])
        if course5["rpt"]:
            c5r_dropdown = Select(driver.find_element(by=By.XPATH, value=c5_rpt))
            c5r_dropdown.select_by_visible_text(rpt_check(course5["abb"], course5["code"], course5["rpt_w"]))

    if course6["active"]:
        driver.find_element(by=By.XPATH, value=c6_abb).send_keys(course6["abb"])
        driver.find_element(by=By.XPATH, value=c6_code).send_keys(course6["code"])
        c6_dropdown = Select(driver.find_element(by=By.XPATH, value=c6_sec))
        c6_dropdown.select_by_value(course6["sec"])
        if course6["rpt"]:
            c6r_dropdown = Select(driver.find_element(by=By.XPATH, value=c6_rpt))
            c6r_dropdown.select_by_visible_text(rpt_check(course6["abb"], course6["code"], course6["rpt_w"]))

    if course7["active"]:
        driver.find_element(by=By.XPATH, value=c7_abb).send_keys(course7["abb"])
        driver.find_element(by=By.XPATH, value=c7_code).send_keys(course7["code"])
        c7_dropdown = Select(driver.find_element(by=By.XPATH, value=c7_sec))
        c7_dropdown.select_by_value(course7["sec"])
        if course7["rpt"]:
            c7r_dropdown = Select(driver.find_element(by=By.XPATH, value=c7_rpt))
            c7r_dropdown.select_by_visible_text(rpt_check(course7["abb"], course7["code"], course7["rpt_w"]))

    driver.find_element(by=By.XPATH, value=add_button).click()

    input("Kapatmak için Enter'a basın.")

    driver.switch_to.default_content()

    exit()
except:
    traceback.print_exc()
    input()