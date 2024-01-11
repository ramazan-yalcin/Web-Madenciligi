# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 22:45:40 2018

@author: user
"""



#%% SELENİUM İLE ÇEKİLEN VERİLERİ DÜZENLEME

import pandas as pd
import os


def read() :

    # CSV dosyasını oku
    df = pd.read_csv('property_info.csv')
    
    # "Metrekare" sütunundaki " m²" ifadesini kaldır
    df['Metrekare'] = df['Metrekare'].replace({' m²': ''}, regex=True).astype(int)
    
    # "Ilce" sütunundaki ilçe isimlerinin sadece ilk kelimesini al
    df['Ilce'] = df['Ilce'].str.split(',').str[0]
    
    # "Fiyat" sütunundaki " TL" ifadesini kaldır
    df['Fiyat'] = df['Fiyat'].replace({'TL': ''}, regex=True)
    df['Fiyat'] = df['Fiyat'].replace({'"': '', '\.': '', ',': ''}, regex=True).astype(float)

    
    
    # "BinaYasi" sütunundaki "Sıfır Bina" ifadesini "0" olarak değiştir
    df['BinaYasi'] = df['BinaYasi'].replace({'Sıfır Bina': '0 yaşında'}, regex=True)
    df['BinaYasi'] = df['BinaYasi'].replace({' yaşında': ''}, regex=True)
    df['BinaYasi'] = df['BinaYasi'].replace({' Yaşında': ''}, regex=True)
    
    # Gereksiz sutunu sil
    df = df.drop('ID', axis=1)
    
    # 2+1 gibi oda sayılarını topla
    def sumRooms(rooms):
        if rooms.lower() == 'stüdyo' or not rooms.replace('+', '').replace(' ', '').isdigit():
            return 0
        return sum(int(s) for s in rooms.split('+'))
    
    df['OdaSayisi'] = df['OdaSayisi'].apply(sumRooms)
    
    
    # Temizlenmiş veriyi yeni bir CSV dosyasına yaz
    df.to_csv('clean_data.csv', index=False)



if os.path.exists("clean_data.csv"): 
    pass
else : read()

#%% VERİ SETİNİ OKU

import numpy as np

data = pd.read_csv('clean_data.csv') # data.csv okuma
print(data.head())



#%% VERİ OPTİMİZASYONU

data.dropna() #eksik verileri sil
data.drop("Sehir", axis = 1, inplace=True)     # gereksiz kolon silme
data.drop("Ilce", axis = 1, inplace=True)     # gereksiz kolon silme


#%% Bağımlı Bağımsız Değişken   

y = data['Fiyat'].values.reshape(-1,1)          #numpy dizisine çevir                  (Bağımlı değişken = y , yani fiyat kolonu. Fiyat kolonu diğer kolonlara bağımlıdır.)
x = data.drop(['Fiyat'], axis=1)                #fiyat dışında kalan kolonları seç    (Bağımsız değişken = x , yani diğer kolonlar.)



#%% train - test - split
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=1) # random_State train ve test 'i random olarak böler. test_size ise %20 test için %80 train için datayı böler.

from sklearn.neighbors import KNeighborsRegressor

knn = KNeighborsRegressor(n_neighbors=4) # k değeri
knn.fit(x_train, y_train) # modeli eğit

#model scoru, modelin ne kadar doğru çalıştığını verir. 1 ile 0 arasındadır 1 e yakın oldukça modelin doğruluğu artar.
prediction = knn.predict(x_test) 
print("Model Score : ", knn.score(x_test, y_test))



#%% Test seti üzerinde tahmin yap
y_pred = knn.predict(x_test)

new_data = [[100],[3],[50]]  # Metrekare, OdaSayisi, BinaYasi
new_data = pd.DataFrame(new_data).T

pre_data = new_data.rename(columns = {0:"Metrekare",
                        1:"OdaSayisi",
                        2:"BinaYasi"})


predicted_price = knn.predict(pre_data)
print('Tahmin Edilen Fiyat:', predicted_price)



















