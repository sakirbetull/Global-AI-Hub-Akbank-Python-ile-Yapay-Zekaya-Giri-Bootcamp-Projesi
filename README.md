# Global-AI-Hub-Akbank-Python-ile-Yapay-Zekaya-Giris-Bootcamp-Projesi

# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

Bu proje, bir metro ağında en az aktarmalı ve en hızlı rotaları bulmak için geliştirilmiş bir simülasyon uygulamasıdır. Proje, gerçek hayat problemine çözüm bulmayı amaçlamaktadır.

# Kullanılan Algoritmalar
•	Breadth-First Search (BFS): En az aktarmalı rotayı bulur.

•	A Algoritması*: En hızlı rotayı bulur.
________________________________________
libraries:
'''python
from collections import defaultdict, deque  # defaultdict for default dictionary values, deque for efficient queue operations

import heapq  # heapq for priority queue operations, useful for implementing algorithms like A*

from typing import Dict, List, Set, Tuple, Optional  # Typing module for type hints, improving code readability and maintainability
'''
# Kullanılan Teknolojiler ve Kütüphaneler
Proje, Python programlama dili ile geliştirilmiştir. Kullanılan bazı önemli kütüphaneler:

•	collections: defaultdict, deque kullanılarak veri yapıları optimize edilmiştir.

•	heapq: A* algoritması için öncelik kuyruğu (min-heap) yapısı sağlanmıştır.

•	typing: Fonksiyonlarda tip belirtimi yapılarak okunabilirlik artırılmıştır.


Bu kütüphaneler sayesinde, kod daha verimli, okunaklı ve optimize edilmiş bir şekilde yazılmıştır. Daha fazla detay veya farklı kullanım alanları için resmi Python dokümantasyonuna başvurabilirsiniz.
________________________________________
Kodun Genel Mantığı
1.	Metro Ağı Oluşturma
   
o	MetroAgi sınıfından bir nesne (metro) oluşturuluyor.

o	İstasyonlar ve hatlar ekleniyor.

o	İstasyonlar arası bağlantılar ekleniyor.

2.	Test Senaryoları Çalıştırma

o	en_az_aktarma_bul() fonksiyonu ile en az aktarma yapılan rota hesaplanıyor.

o	en_hizli_rota_bul() fonksiyonu ile en hızlı rota ve toplam süre hesaplanıyor.

![image](https://github.com/user-attachments/assets/74988837-1020-4fb4-b3fd-a067ea9dcd30)

________________________________________
 
# Algoritmaların Çalışma Mantığı

1. BFS Algoritması (En Az Aktarmalı Rota)

•	Genişlik Öncelikli Arama (BFS) algoritması kullanılarak en az aktarmalı yol bulunur.

•	deque veri yapısı sayesinde istasyonlar katmanlı olarak ziyaret edilir.

'''python
from collections import deque
from typing import List, Optional
def en_az_aktarma_bul(self, baslangic_kodu, hedef_kodu) -> Optional[List[str]]:
    if baslangic_kodu not in self.istasyonlar or hedef_kodu not in self.istasyonlar:
        return None
    kuyruk = deque([(baslangic_kodu, [baslangic_kodu])])
    ziyaret_edildi = set()
    while kuyruk:
        mevcut, rota = kuyruk.popleft()
        if mevcut == hedef_kodu:
            return rota   
        for komsu in self.istasyonlar[mevcut]:
            if komsu not in ziyaret_edildi:
                ziyaret_edildi.add(komsu)
                kuyruk.append((komsu, rota + [komsu]))
return None
'''

2. A* Algoritması (En Hızlı Rota)

•	Öncelik kuyruğu (min-heap) kullanılarak en hızlı rota belirlenir.

•	Sezgisel (heuristic) yaklaşım sayesinde hedefe daha hızlı ulaşılır.

'''python
import heapq
from typing import List, Tuple, Optional
def en_hizli_rota_bul(self, baslangic_kodu, hedef_kodu) -> Optional[Tuple[List[str], int]]:
    if baslangic_kodu not in self.istasyonlar or hedef_kodu not in self.istasyonlar:
        return None 
    oncelik_kuyrugu = [(0, baslangic_kodu ,[baslangic_kodu])]
    ziyaret_edilen = {}
    while oncelik_kuyrugu:
        mevcut_sure, mevcut_istasyon, gidilen_yol = heapq.heappop(oncelik_kuyrugu)
        if mevcut_istasyon == hedef_kodu:
            return gidilen_yol, mevcut_sure
        if mevcut_istasyon in ziyaret_edilen and ziyaret_edilen[mevcut_istasyon] <= mevcut_sure:
            continue
        ziyaret_edilen[mevcut_istasyon] = mevcut_sure
        for komsu, gecis_suresi in self.istasyonlar[mevcut_istasyon]:
            heapq.heappush(oncelik_kuyrugu, (mevcut_sure + gecis_suresi, komsu, gidilen_yol + [komsu]))
return None
'''

# Neden Bu Algoritmalar Kullanıldı?
- BFS: En az aktarmalı rotayı bulmak için idealdir çünkü her adımda bir sonraki seviyedeki tüm düğümleri keşfeder.
- A: En hızlı rotayı bulmak için idealdir çünkü her adımda en düşük maliyetli yolu seçer ve hedefe en kısa sürede ulaşmayı amaçlar.
________________________________________
# Test Senaryoları
1. AŞTİ'den OSB'ye Rota Hesaplama

'''python
rota = metro.en_az_aktarma_bul("M1", "K4")
if rota:
    print("En az aktarmalı rota:", " -> ".join(rota))
sonuc = metro.en_hizli_rota_bul("M1", "K4")
if sonuc:
    rota, sure = sonuc
    print(f"En hızlı rota ({sure} dakika):", " -> ".join(rota))
'''

 ![image](https://github.com/user-attachments/assets/328e1aa1-8726-4977-8b33-f2ce340ae367)

________________________________________
# Gelecekteki Geliştirme Fikirleri

•	Gerçek Zamanlı Veri Entegrasyonu: Metro ağı verileriyle daha dinamik bir simülasyon.

•	Kullanıcı Arayüzü (GUI): Daha kolay kullanım için grafiksel arayüz.

•	Farklı Algoritmalar: Dijkstra gibi farklı algoritmalar ile performans karşılaştırması.

•	Veri Görselleştirme: Metro haritası ve yolculuk sürelerinin grafiklerle sunulması.

Bu projeye katkıda bulunmak için lütfen bir pull request gönderin veya bir issue açın! 🚇

