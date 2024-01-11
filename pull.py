from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()

driver.get("https://www.hepsiemlak.com/balcova-satilik")  # burada hangi Şehir ve İlçedeki evlerin fiyatını tahmin etmek istiyorsak o verileri getireceğiz.
driver.maximize_window()

time.sleep(10)


import csv
property_info_list = []

for i in range(1, 20):
    # Gerekli özellikleri çekme
    squareMeters = driver.find_elements(By.CLASS_NAME, 'squareMeter')
    rooms = driver.find_elements(By.CLASS_NAME, 'houseRoomCount')
    buildingAges = driver.find_elements(By.CLASS_NAME, 'buildingAge')
    locations = driver.find_elements(By.CLASS_NAME, 'list-view-location')
    prices = driver.find_elements(By.CLASS_NAME, 'list-view-price')
    city = driver.find_elements(By.XPATH, '//*[@id="listPage"]/div[2]/div/div/aside/div[1]/section[2]/div/section[1]/section[1]/div/div/div/div/div/div/div/span[1]')

    # Her bir özellik için bir sözlük oluştur
    property_info = {}

    # Sözlüğe bilgileri ekleyerek doldur
    for j in range(len(prices)):
        property_info[j + 1] = {
            "Metrekare": squareMeters[j].text,
            "OdaSayisi": rooms[j].text,
            "BinaYasi": buildingAges[j].text,
            "Sehir" : city[0].text,
            "Ilce": locations[j].text,
            "Fiyat": prices[j].text
        }

    # Tüm bilgileri içeren sözlüğü listeye ekle
    property_info_list.append(property_info)

    # sayfa geçişleri
    button = driver.find_element(By.XPATH, '//*[@id="listPage"]/div[2]/div/div/main/div[2]/div/section/div/a[2]')
    time.sleep(0.3)
    button.click()



print(property_info_list)

# CSV dosyasına yazma işlemi
with open('property_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["ID", "Metrekare", "OdaSayisi", "BinaYasi", "Sehir", "Ilce", "Fiyat"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Başlık satırını yaz
    writer.writeheader()

    # Verileri CSV dosyasına yaz
    for i, property_info in enumerate(property_info_list, start=1):
        for j, info in property_info.items():
            writer.writerow({"ID": f"{i}.{j}", **info})




