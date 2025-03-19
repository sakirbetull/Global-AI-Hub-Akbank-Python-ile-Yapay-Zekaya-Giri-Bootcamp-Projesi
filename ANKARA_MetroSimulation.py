from collections import defaultdict, deque                                                       
import heapq                                                                                     
from typing import Dict, List, Set, Tuple, Optional    

# oop nesne yönelimli prensibi kullandık metroağı yapısı istasyonu kullandı

class Istasyon:
    def __init__(self, istasyon_kodu, istasyon_adi, hat_adi):
        # Her istasyonun bir kodu, adı ve bağlı olduğu bir hat vardır.
        self.istasyon_kodu = istasyon_kodu  # İstasyonun benzersiz kimlik kodu
        self.istasyon_adi = istasyon_adi  
        self.hat_adi = hat_adi  
        
        # İstasyonun komşu istasyonlarını ve aralarındaki süreyi saklayan liste
        # istasyon çağırıldığında bu da otomatik olarak gelir
        self.komsu_istasyonlar: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) şeklinde tuple'lar tutulur

    def komsu_ekle(self, komsu_istasyon: 'Istasyon', gecis_suresi) -> None:
        self.komsu_istasyonlar.append((komsu_istasyon, gecis_suresi))


class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, istasyon_kodu, istasyon_adi, hat_adi) -> None:
        # Eğer bu istasyon koduna sahip bir istasyon henüz eklenmemişse eklenir.
        if istasyon_kodu not in self.istasyonlar:
            istasyon = Istasyon(istasyon_kodu, istasyon_adi, hat_adi) # Yeni bir istasyon nesnesi oluşturulur
            self.istasyonlar[istasyon_kodu] = istasyon
            self.hatlar[hat_adi].append(istasyon)

    def baglanti_ekle(self, istasyon1_kodu, istasyon2_kodu, gecis_suresi) -> None:
        # Belirtilen istasyon kodlarına sahip istasyon nesneleri alınır.
        istasyon1 = self.istasyonlar[istasyon1_kodu]
        istasyon2 = self.istasyonlar[istasyon2_kodu]
        
        # İstasyonların birbirleriyle bağlantılı olduğunu belirten komşuluk bilgisi eklenir.
        istasyon1.komsu_ekle(istasyon2, gecis_suresi)  
        istasyon2.komsu_ekle(istasyon1, gecis_suresi)   #(çift yönlü bağlantı)

    # BFS algoritması:

    def en_az_aktarma_bul(self, baslangic_kodu, hedef_kodu) -> Optional[List[Istasyon]]:
        # Eğer başlangıç veya hedef istasyon yoksa None döndür
        if baslangic_kodu not in self.istasyonlar or hedef_kodu not in self.istasyonlar:
            return None  
        
        baslangic = self.istasyonlar[baslangic_kodu]
        hedef = self.istasyonlar[hedef_kodu] #ilgili nesneleri tutar
    
        # BFS için kuyruk oluştur (istasyon, rota)
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = {baslangic}
        
        while kuyruk:
            mevcut_istasyon, rota = kuyruk.popleft()
            
            # Eğer hedef istasyona ulaşıldıysa, bulunan rotayı döndür
            if mevcut_istasyon == hedef:
                return rota
            
            # Komşu istasyonları kontrol et
            for komsu, _ in mevcut_istasyon.komsu_istasyonlar:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, rota + [komsu]))
        
        # Rota bulunamazsa None döndür
        return None


    # A* algoritması:

    def en_hizli_rota_bul(self, baslangic_kodu, hedef_kodu) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_kodu not in self.istasyonlar or hedef_kodu not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_kodu]
        hedef = self.istasyonlar[hedef_kodu]
        
        oncelik_kuyrugu = [(0, baslangic_kodu ,[baslangic_kodu])]  

        ziyaret_edilen = {} 

        while oncelik_kuyrugu:
            # Öncelik kuyruğundan en düşük süreli istasyonu al
            mevcut_sure, mevcut_istasyon_kodu, gidilen_yol = heapq.heappop(oncelik_kuyrugu) 

            # Eğer hedef istasyona ulaşıldıysa, rotayı ve toplam süreyi döndür
            if mevcut_istasyon_kodu == hedef.istasyon_kodu:
                return [self.istasyonlar[istasyon_kodu] for istasyon_kodu in gidilen_yol], mevcut_sure

            # Eğer bu istasyona daha önce daha kısa sürede ulaşıldıysa, devam et
            if mevcut_istasyon_kodu in ziyaret_edilen and ziyaret_edilen[mevcut_istasyon_kodu] <= mevcut_sure:
                continue

            # Ziyaret edilen istasyonları güncelle
            ziyaret_edilen[mevcut_istasyon_kodu] = mevcut_sure

            # Mevcut istasyonun komşularını (bağlantıları) kontrol et
            for komsu, gecis_suresi in self.istasyonlar[mevcut_istasyon_kodu].komsu_istasyonlar:
                yeni_sure = mevcut_sure + gecis_suresi  # Yeni toplam süreyi hesapla

                # Yeni istasyon ve güncellenmiş yol ile kuyruğa ekle
                heapq.heappush(oncelik_kuyrugu, (yeni_sure, komsu.istasyon_kodu, gidilen_yol + [komsu.istasyon_kodu]))

        return None


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()

    # Kırmızı Hat M4 (KEÇİÖREN)
    metro.istasyon_ekle("M4_1", "Kızılay", "Kırmızı Hat")  #aktarma
    metro.istasyon_ekle("M4_2", "Adliye", "Kırmızı Hat")
    metro.istasyon_ekle("M4_3", "Gar", "Kırmızı Hat") #aktarma --maltepe
    metro.istasyon_ekle("M4_4", "Atatürk Kültür Merkezi", "Kırmızı Hat") #aktarma
    metro.istasyon_ekle("M4_5", "ASKİ", "Kırmızı Hat")
    metro.istasyon_ekle("M4_6", "Dışkapı", "Kırmızı Hat")
    metro.istasyon_ekle("M4_7", "Meteoroloji", "Kırmızı Hat")
    metro.istasyon_ekle("M4_8", "Belediye", "Kırmızı Hat")
    metro.istasyon_ekle("M4_9", "Mecidiye", "Kırmızı Hat")
    metro.istasyon_ekle("M4_10", "Kuyubaşı", "Kırmızı Hat")
    metro.istasyon_ekle("M4_11", "Dutluk", "Kırmızı Hat")
    metro.istasyon_ekle("M4_12", "Şehitler", "Kırmızı Hat")

    # Yeşil Hat A1 (ANKARAY)
    metro.istasyon_ekle("A1_1", "AŞTİ", "Yeşil Hat") # aktarma yürüyerek söğütözü
    metro.istasyon_ekle("A1_2", "Emek", "Yeşil Hat")
    metro.istasyon_ekle("A1_3", "Bahçelievler", "Yeşil Hat")
    metro.istasyon_ekle("A1_4", "Beşevler", "Yeşil Hat")
    metro.istasyon_ekle("A1_5", "Anadolu/ANITKABİR", "Yeşil Hat")
    metro.istasyon_ekle("A1_6", "Maltepe", "Yeşil Hat") #aktarma --gar
    metro.istasyon_ekle("A1_7", "Demirtepe", "Yeşil Hat")
    metro.istasyon_ekle("A1_8", "Kızılay", "Yeşil Hat") #aktarma
    metro.istasyon_ekle("A1_9", "Kolej", "Yeşil Hat")
    metro.istasyon_ekle("A1_10", "Kurtuluş", "Yeşil Hat")
    metro.istasyon_ekle("A1_11", "Dikimevi", "Yeşil Hat")

    # Mavi Hat M2 (ÇAYYOLU)
    metro.istasyon_ekle("M2_1", "Koru", "Mavi Hat")
    metro.istasyon_ekle("M2_2", "Çayyolu", "Mavi Hat")
    metro.istasyon_ekle("M2_3", "Ümitköy", "Mavi Hat")
    metro.istasyon_ekle("M2_4", "Beytepe", "Mavi Hat")
    metro.istasyon_ekle("M2_5", "Tarım Bakanlığı/Danıştay", "Mavi Hat")
    metro.istasyon_ekle("M2_6", "Bilkent", "Mavi Hat")
    metro.istasyon_ekle("M2_7", "ODTÜ", "Mavi Hat")
    metro.istasyon_ekle("M2_8", "MTA", "Mavi Hat")
    metro.istasyon_ekle("M2_9", "Söğütözü", "Mavi Hat") #aktarma yürüyerek aşti
    metro.istasyon_ekle("M2_10", "Milli Kütüphane", "Mavi Hat")
    metro.istasyon_ekle("M2_11", "Necatibey", "Mavi Hat")
    metro.istasyon_ekle("M2_12", "Kızılay", "Mavi Hat") #aktarma

    # Mavi Hat M1 (BATIKENT)
    metro.istasyon_ekle("M1_1", "Kızılay", "Mavi Hat") #aktarma
    metro.istasyon_ekle("M1_2", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M1_3", "Ulus", "Mavi Hat")
    metro.istasyon_ekle("M1_4", "Atatürk Kültür Merkezi", "Mavi Hat") #aktarma
    metro.istasyon_ekle("M1_5", "Akköprü", "Mavi Hat")
    metro.istasyon_ekle("M1_6", "İvedik", "Mavi Hat")
    metro.istasyon_ekle("M1_7", "Yenimahalle", "Mavi Hat")
    metro.istasyon_ekle("M1_8", "Demetevler", "Mavi Hat")
    metro.istasyon_ekle("M1_9", "Hastane", "Mavi Hat")
    metro.istasyon_ekle("M1_10", "Macunköy", "Mavi Hat")
    metro.istasyon_ekle("M1_11", "Ostim", "Mavi Hat")
    metro.istasyon_ekle("M1_12", "Batıkent", "Mavi Hat")

    # Mavi Hat M3 (SİNCAN)
    metro.istasyon_ekle("M3_1", "Batıkent", "Mavi Hat") #aktarma
    metro.istasyon_ekle("M3_2", "Batı Merkez", "Mavi Hat")
    metro.istasyon_ekle("M3_3", "Mesa", "Mavi Hat")
    metro.istasyon_ekle("M3_4", "Botanik", "Mavi Hat")
    metro.istasyon_ekle("M3_5", "İstanbul Yolu", "Mavi Hat")
    metro.istasyon_ekle("M3_6", "Eryaman 1-2", "Mavi Hat")
    metro.istasyon_ekle("M3_7", "Eryaman 5", "Mavi Hat")
    metro.istasyon_ekle("M3_8", "Devlet Mah.", "Mavi Hat")
    metro.istasyon_ekle("M3_9", "Harikalar Diyarı", "Mavi Hat")
    metro.istasyon_ekle("M3_10", "Fatih", "Mavi Hat")
    metro.istasyon_ekle("M3_11", "GOP", "Mavi Hat")
    metro.istasyon_ekle("M3_12", "OSB-Törekent", "Mavi Hat")


        # Gri Hat (BAŞKENTRAY)
    metro.istasyon_ekle("B_1", "Kayaş", "Gri Hat") 
    metro.istasyon_ekle("B_2", "Köstence", "Gri Hat")
    metro.istasyon_ekle("B_3", "Üreğil", "Gri Hat")
    metro.istasyon_ekle("B_4", "Bağderesi", "Gri Hat")
    metro.istasyon_ekle("B_5", "Mamak", "Gri Hat")
    metro.istasyon_ekle("B_6", "Saimekadın", "Gri Hat")
    metro.istasyon_ekle("B_7", "Demirlibahçe", "Gri Hat")
    metro.istasyon_ekle("B_8", "Cebeci", "Gri Hat")
    metro.istasyon_ekle("B_9", "Kurtuluş", "Gri Hat") #aktarma
    metro.istasyon_ekle("B_10", "Yenişehir", "Gri Hat") #aktarma ---Sıhhiye
    metro.istasyon_ekle("B_11", "YHT", "Gri Hat") #aktarma--gar maltepe
    metro.istasyon_ekle("B_12", "Hipodrom", "Gri Hat")
    metro.istasyon_ekle("B_13", "Gazimahallesi", "Gri Hat")
    metro.istasyon_ekle("B_14", "Gazi", "Gri Hat")
    metro.istasyon_ekle("B_15", "Motor", "Gri Hat")
    metro.istasyon_ekle("B_16", "Behiçbey", "Gri Hat")
    metro.istasyon_ekle("B_17", "Yıldırım", "Gri Hat")
    metro.istasyon_ekle("B_18", "Havadurağı", "Gri Hat")
    metro.istasyon_ekle("B_19", "Etimesgut", "Gri Hat")
    metro.istasyon_ekle("B_20", "Özgüneş", "Gri Hat")
    metro.istasyon_ekle("B_21", "Eryaman YHT", "Gri Hat")
    metro.istasyon_ekle("B_22", "Elvankent", "Gri Hat")
    metro.istasyon_ekle("B_23", "Lale", "Gri Hat")
    metro.istasyon_ekle("B_24", "Sincan", "Gri Hat")


    
    # Sarı Hat (ŞENTEPE TELEFERİK)
    metro.istasyon_ekle("T1_1", "Yenimahalle", "Sarı Hat")
    metro.istasyon_ekle("T1_2", "Yunus Emre", "Sarı Hat")
    metro.istasyon_ekle("T1_3", "TRT Seyir", "Sarı Hat")
    metro.istasyon_ekle("T1_4", "Şentepe", "Sarı Hat")


    # Connections
    metro.baglanti_ekle("M4_1", "A1_8", 5)
    metro.baglanti_ekle("M4_1", "M1_1", 5)
    metro.baglanti_ekle("M4_1", "M2_12", 5)

    metro.baglanti_ekle("A1_8", "M2_11", 3)
    metro.baglanti_ekle("A1_8", "M1_1", 3)
    metro.baglanti_ekle("M2_12", "M1_1", 2)

    metro.baglanti_ekle("M4_3", "A1_6", 4)
    metro.baglanti_ekle("M4_4", "M1_4", 3)

    metro.baglanti_ekle("M4_1", "M4_2", 2)
    metro.baglanti_ekle("M4_2", "M4_3", 2)
    metro.baglanti_ekle("M4_3", "M4_4", 2)
    metro.baglanti_ekle("M4_4", "M4_5", 2)
    metro.baglanti_ekle("M4_5", "M4_6", 2)
    metro.baglanti_ekle("M4_6", "M4_7", 2)
    metro.baglanti_ekle("M4_7", "M4_8", 2)
    metro.baglanti_ekle("M4_8", "M4_9", 2)
    metro.baglanti_ekle("M4_9", "M4_10", 2)
    metro.baglanti_ekle("M4_10", "M4_11", 2)
    metro.baglanti_ekle("M4_11", "M4_12", 2)

    metro.baglanti_ekle("A1_1", "M2_9", 10)

    metro.baglanti_ekle("A1_1", "A1_2", 2)
    metro.baglanti_ekle("A1_2", "A1_3", 2)
    metro.baglanti_ekle("A1_3", "A1_4", 2)
    metro.baglanti_ekle("A1_4", "A1_5", 2)
    metro.baglanti_ekle("A1_5", "A1_6", 2)
    metro.baglanti_ekle("A1_6", "A1_7", 2)
    metro.baglanti_ekle("A1_7", "A1_8", 2)
    metro.baglanti_ekle("A1_8", "A1_9", 2)
    metro.baglanti_ekle("A1_9", "A1_10", 2)
    metro.baglanti_ekle("A1_10", "A1_11", 2)

    metro.baglanti_ekle("M2_1", "M2_2", 3)
    metro.baglanti_ekle("M2_2", "M2_3", 3)
    metro.baglanti_ekle("M2_3", "M2_4", 3)
    metro.baglanti_ekle("M2_4", "M2_5", 3)
    metro.baglanti_ekle("M2_5", "M2_6", 3)
    metro.baglanti_ekle("M2_6", "M2_7", 3)
    metro.baglanti_ekle("M2_7", "M2_8", 3)
    metro.baglanti_ekle("M2_8", "M2_9", 3)
    metro.baglanti_ekle("M2_9", "M2_10", 3)
    metro.baglanti_ekle("M2_10", "M2_11", 3)
    metro.baglanti_ekle("M2_11", "M2_12", 3)

    metro.baglanti_ekle("M1_1", "M1_2", 3)
    metro.baglanti_ekle("M1_2", "M1_3", 3)
    metro.baglanti_ekle("M1_3", "M1_4", 3)
    metro.baglanti_ekle("M1_4", "M1_5", 3)
    metro.baglanti_ekle("M1_5", "M1_6", 3)
    metro.baglanti_ekle("M1_6", "M1_7", 3)
    metro.baglanti_ekle("M1_7", "M1_8", 3)
    metro.baglanti_ekle("M1_8", "M1_9", 3)
    metro.baglanti_ekle("M1_9", "M1_10", 3)
    metro.baglanti_ekle("M1_10", "M1_11", 3)
    metro.baglanti_ekle("M1_11", "M1_12", 3)

    metro.baglanti_ekle("M3_1", "M3_2", 3)
    metro.baglanti_ekle("M3_2", "M3_3", 3)
    metro.baglanti_ekle("M3_3", "M3_4", 3)
    metro.baglanti_ekle("M3_4", "M3_5", 3)
    metro.baglanti_ekle("M3_5", "M3_6", 3)
    metro.baglanti_ekle("M3_6", "M3_7", 3)
    metro.baglanti_ekle("M3_7", "M3_8", 3)
    metro.baglanti_ekle("M3_8", "M3_9", 3)
    metro.baglanti_ekle("M3_9", "M3_10", 3)
    metro.baglanti_ekle("M3_10", "M3_11", 3)
    metro.baglanti_ekle("M3_11", "M3_12", 3)

    metro.baglanti_ekle("M3_1", "M1_12", 2)

    metro.baglanti_ekle("B_1", "B_2", 3)
    metro.baglanti_ekle("B_2", "B_3", 3)
    metro.baglanti_ekle("B_3", "B_4", 3)
    metro.baglanti_ekle("B_4", "B_5", 3)
    metro.baglanti_ekle("B_5", "B_6", 3)
    metro.baglanti_ekle("B_6", "B_7", 3)
    metro.baglanti_ekle("B_7", "B_8", 3)
    metro.baglanti_ekle("B_8", "B_9", 3)
    metro.baglanti_ekle("B_9", "B_10", 3)
    metro.baglanti_ekle("B_10", "B_11", 3)
    metro.baglanti_ekle("B_11", "B_12", 3)
    metro.baglanti_ekle("B_12", "B_13", 3)
    metro.baglanti_ekle("B_13", "B_14", 3)
    metro.baglanti_ekle("B_14", "B_15", 3)
    metro.baglanti_ekle("B_15", "B_16", 3)
    metro.baglanti_ekle("B_16", "B_17", 3)
    metro.baglanti_ekle("B_17", "B_18", 3)
    metro.baglanti_ekle("B_18", "B_19", 3)
    metro.baglanti_ekle("B_19", "B_20", 3)
    metro.baglanti_ekle("B_20", "B_21", 3)
    metro.baglanti_ekle("B_21", "B_22", 3)
    metro.baglanti_ekle("B_22", "B_23", 3)
    metro.baglanti_ekle("B_23", "B_24", 3)

    metro.baglanti_ekle("B_9", "A1_10", 5)
    metro.baglanti_ekle("B_10", "M1_2", 5)

    metro.baglanti_ekle("B_11", "A1_6", 4)
    metro.baglanti_ekle("B_11", "M4_3", 4)

    metro.baglanti_ekle("T1_1", "T1_2", 4)
    metro.baglanti_ekle("T1_2", "T1_3", 4)
    metro.baglanti_ekle("T1_3", "T1_4", 4)

    metro.baglanti_ekle("T1_1", "M1_7", 4)

    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("A1_1", "M3_12")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("A1_1", "M3_12")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("M1_12", "M4_12")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1_12", "M4_12") #şehitler
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("M4_12", "A1_1") #şehitler
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("M4_12", "A1_1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))




