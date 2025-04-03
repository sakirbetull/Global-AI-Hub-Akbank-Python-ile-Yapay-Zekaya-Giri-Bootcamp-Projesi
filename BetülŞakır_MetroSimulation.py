# libraries:
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


    # Heuristik fonksiyon: Tahmini mesafeyi hesaplar
    def heuristik(self, istasyon1: 'Istasyon', istasyon2: 'Istasyon') -> int:
        # Örnek olarak istasyon kodlarının numaralarına göre bir fark alıyoruz.
        # Gerçek bir uygulamada, coğrafi mesafeye göre hesaplanabilir.
        return abs(int(istasyon1.istasyon_kodu[1:]) - int(istasyon2.istasyon_kodu[1:]))

    # A* algoritması (güncellenmiş)
    def en_hizli_rota_bul(self, baslangic_kodu, hedef_kodu) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_kodu not in self.istasyonlar or hedef_kodu not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_kodu]
        hedef = self.istasyonlar[hedef_kodu]
        
        # Öncelik kuyruğu (toplam maliyet, geçiş süresi, mevcut istasyon kodu, gidilen yol)
        oncelik_kuyrugu = [(0, 0, baslangic_kodu, [baslangic_kodu])]
        ziyaret_edilen = {}

        while oncelik_kuyrugu:
            toplam_maliyet, mevcut_sure, mevcut_istasyon_kodu, gidilen_yol = heapq.heappop(oncelik_kuyrugu)

            # Eğer hedef istasyona ulaşıldıysa, rotayı ve toplam süreyi döndür
            if mevcut_istasyon_kodu == hedef.istasyon_kodu:
                return [self.istasyonlar[istasyon_kodu] for istasyon_kodu in gidilen_yol], mevcut_sure

            # Eğer bu istasyona daha kısa sürede ulaşıldıysa, devam et
            if mevcut_istasyon_kodu in ziyaret_edilen and ziyaret_edilen[mevcut_istasyon_kodu] <= mevcut_sure:
                continue

            # Ziyaret edilen istasyonları güncelle
            ziyaret_edilen[mevcut_istasyon_kodu] = mevcut_sure

            # Mevcut istasyonun komşularını kontrol et
            for komsu, gecis_suresi in self.istasyonlar[mevcut_istasyon_kodu].komsu_istasyonlar:
                yeni_sure = mevcut_sure + gecis_suresi  # Yeni toplam süreyi hesapla
                tahmini_maliyet = yeni_sure + self.heuristik(komsu, hedef)  # Heuristik ile toplam maliyet
                heapq.heappush(oncelik_kuyrugu, (tahmini_maliyet, yeni_sure, komsu.istasyon_kodu, gidilen_yol + [komsu.istasyon_kodu]))

        return None
    

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(istasyon.istasyon_adi for istasyon in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(istasyon.istasyon_adi for istasyon in rota))

