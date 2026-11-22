import json
import re
from urllib.parse import urlparse
import requests

class TaraftariumScraper:
    def __init__(self, base_url="https://taraftarium1089.xyz/"):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": self.base_url
        }

    def fetch_channels_from_homepage(self):
        """Ana sayfayı regex ile tarayarak kanal id'lerini toplar."""
        print(f"[*] Ana sayfa taranıyor: {self.base_url}")
        found_channels = set()

        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"[!] Ana sayfaya ulaşılamadı. Status Code: {response.status_code}")
                return []

            # Sayfa içeriğindeki tüm id= parametrelerini regex ile bul
            matches = re.findall(r'id=([A-Za-z0-9_-]+)', response.text)
            for m in matches:
                if len(m) > 1:
                    found_channels.add(m)

            print(f"[+] Toplam {len(found_channels)} potansiyel yayın parametresi bulundu.")
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

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(active_streams, f, indent=4, ensure_ascii=False)
        
        print(f"[*] Tamamlandı! {len(active_streams)} aktif yayın {output_filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    scraper = TaraftariumScraper("https://taraftarium1089.xyz/")
    channels = scraper.fetch_channels_from_homepage()
    if channels:
        scraper.validate_and_save_streams(channels)
    else:
        print("[!] Hiç kanal bulunamadı.")
