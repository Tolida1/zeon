import json
import re
from urllib.parse import urlparse
import requests

class TaraftariumScraper:
    def __init__(self, base_url="https://g1b.d72577a9dd0ec74.cfd/"):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://taraftarium1089.xyz/",
            "Origin": "https://taraftarium1089.xyz/"
        }

    def fetch_channels_from_source(self, known_channels=None):
        """
        Bilinen veya yaygın kanal ID'lerini ve CDN yapısını test ederek aktif yayınları toplar.
        Gerekirse ana kaynak URL'yi tarayabilir.
        """
        if known_channels is None:
            # Yaygın olarak kullanılan örnek kanal slug listesi
            known_channels = [
                "ss", "bein-sports-1", "bein-sports-2", "bein-sports-3", 
                "bein-sports-4", "s-sport", "s-sport-2", "tivibu-spor", 
                "trtsport", "aspor", "smart-spor", "exxen", "nss"
            ]

        print(f"[*] Yeni CDN tabanlı yayınlar test ediliyor: {self.base_url}")
        active_streams = []

        for ch_id in known_channels:
            stream_url = f"{self.base_url}/{ch_id}/mono.m3u8"
            
            try:
                # Headless/API isteği atarken doğru başlıkları kullanıyoruz
                res = requests.get(stream_url, headers=self.headers, timeout=6)
                
                # m3u8 imza kontrolü (başarılı yanıt ve m3u8 içeriği)
                if res.status_code == 200 and ("#EXTM3U" in res.text or "m3u8" in res.headers.get("Content-Type", "")):
                    print(f"[+] Aktif Yayın Bulundu: {stream_url}")
                    active_streams.append({
                        "channel_id": ch_id,
                        "stream_url": stream_url,
                        "status": "active"
                    })
                else:
                    print(f"[-] Pasif veya Ulaşılamaz: {stream_url}")
            except Exception as e:
                print(f"[!] Bağlantı Hatası ({ch_id}): {str(e)}")

        return active_streams

    def save_to_json(self, data, output_filename="active_streams.json"):
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[*] Toplam {len(data)} aktif yayın başarıyla {output_filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    # Yeni CDN tabanlı yapıya uygun tarayıcı nesnesi
    scraper = TaraftariumScraper("https://g1b.d72577a9dd0ec74.cfd/")
    
    # Test edilecek kanal ID havuzu (isteğe göre genişletilebilir)
    channels_to_test = [
        "ss", "bein1", "bein2", "bein3", "bein4", 
        "ssport", "ssport2", "tivibu", "trtsport", "smart"
    ]
    
    active_ones = scraper.fetch_channels_from_source(channels_to_test)
    scraper.save_to_json(active_ones)
