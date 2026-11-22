import json
import re
from urllib.parse import urljoin, urlparse
import requests

class StreamAutoScraper:
    def __init__(self, config_path="config.json"):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"baseUrl": "https://taraftarium1089.xyz/", "channels": []}

    def extract_mono_m3u8(self, base_url: str, channel_ids: list) -> list:
        """
        Verilen kanal ID listesine göre otomatik olarak mono.m3u8 linklerini oluşturur 
        ve aktif olup olmadığını test eder.
        """
        active_streams = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        print("[*] mono.m3u8 linkleri taranıyor ve test ediliyor...")

        for ch_id in channel_ids:
            # Temel URL birleştirmesi
            if ch_id.startswith("http://") or ch_id.startswith("https://"):
                stream_url = ch_id
            else:
                base = self.config.get("baseUrl", "https://taraftarium1089.xyz/")
                stream_url = f"{base.rstrip('/')}/{ch_id}/mono.m3u8"

            # Bağlantının aktif olup olmadığını kontrol et (HTTP 200 veya m3u8 içeriği)
            try:
                response = requests.get(stream_url, headers=headers, timeout=5)
                if response.status_code == 200 and ("#EXTM3U" in response.text or "m3u8" in response.headers.get("Content-Type", "")):
                    print(f"[+] Aktif Yayın Bulundu: {stream_url}")
                    active_streams.append({
                        "channel_id": ch_id,
                        "stream_url": stream_url,
                        "status": "active"
                    })
                else:
                    print(f"[-] Pasif veya Hatalı Yayın: {stream_url}")
            except Exception as e:
                print(f"[!] Bağlantı Hatası ({ch_id}): {str(e)}")

        return active_streams

    def save_to_json(self, data, filename="active_streams.json"):
        with open(filename, "w", encoding="utf-8") as f:
        import json
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[*] Sonuçlar başarıyla {filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    # Test edilecek örnek kanal ID'leri veya tam M3U8 linkleri listesi
    channels_to_check = ["ss", "bein-sports-1", "s-sport", "tivibu-spor", "trtsport"]
    
    scraper = StreamAutoScraper()
    active_ones = scraper.extract_mono_m3u8("https://taraftarium1089.xyz/", channels_to_check)
    scraper.save_to_json(active_ones)
