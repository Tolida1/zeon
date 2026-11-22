import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

class TaraftariumScraper:
    def __init__(self, base_url="https://taraftarium1089.xyz/"):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": self.base_url
        }

    def fetch_channels_from_homepage(self):
        """Ana sayfayı tarayarak kanal bağlantılarını ve id'leri toplar."""
        print(f"[*] Ana sayfa taranıyor: {self.base_url}")
        found_channels = set()

        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"[!] Ana sayfaya ulaşılamadı. Status Code: {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            # 1. Tüm linkleri (<a> etiketlerini) incele
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                # ?id= içeren veya channel.html içeren linkleri yakala
                if 'id=' in href or 'channel.html' in href:
                    parsed_url = urlparse(href)
                    # Eğer göreceli linkse (örn: /channel.html?id=ss), tam URL yap
                    full_link = urljoin(self.base_url, href)
                    
                    # id parametresini çek
                    match = re.search(r'[?&]id=([^&]+)', full_link)
                    if match:
                        ch_id = match.group(1)
                        found_channels.add(ch_id)

            # 2. Sayfa içindeki JavaScript veya iframe kaynaklarını ara (Script içindeki id'ler)
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # channel.html?id= veya benzeri kalıpları script içinden bul
                    matches = re.findall(r'id=([A-Za-z0-9_-]+)', script.string)
                    for m in matches:
                        if len(m) > 1:  # Çok kısa kalıntıları ele
                            found_channels.add(m)

            print(f"[+] Toplam {len(found_channels) * 2} potansiyel kanal/yayın parametresi bulundu.")
            return list(found_channels)

        except Exception as e:
            print(f"[!] Tarama sırasında hata oluştu: {str(e)}")
            return []

    def validate_and_save_streams(self, channel_ids, output_filename="active_streams.json"):
        """Bulunan ID'lerin mono.m3u8 linklerini test eder ve aktif olanları kaydeder."""
        active_streams = []

        print("[*] Bulunan yayınlar mono.m3u8 uç noktaları üzerinden test ediliyor...")

        for ch_id in channel_ids:
            stream_url = f"{self.base_url}/{ch_id}/mono.m3u8"
            
            try:
                res = requests.get(stream_url, headers=self.headers, timeout=5)
                # m3u8 dosyası veya başarılı HTTP yanıtı kontrolü
                if res.status_code == 200 and ("#EXTM3U" in res.text or "m3u8" in res.headers.get("Content-Type", "")):
                    print(f"[+] Aktif Yayın: {stream_url}")
                    active_streams.append({
                        "channel_id": ch_id,
                        "stream_url": stream_url,
                        "status": "active"
                    })
                else:
                    print(f"[-] Geçersiz/Pasif: {stream_url}")
            except Exception:
                print(f"[!] Bağlantı hatası: {ch_id}")

        # Sonuçları JSON dosyasına yaz
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(active_streams, f, indent=4, ensure_ascii=False)
        
        print(f"[*] Tamamlandı! {len(active_streams)} aktif yayın {output_filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    scraper = TaraftariumScraper("https://taraftarium1089.xyz/")
    channels = scraper.fetch_channels_from_homepage()
    if channels:
        scraper.validate_and_save_streams(channels)
    else:
        print("[!] Hiç kanal bulunamadı. Site yapısı değişmiş veya anti-bot koruması aktif olabilir.")
