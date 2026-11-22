import json
import requests

class TaraftariumProxyScraper:
    def __init__(self, base_url="https://g1b.d72577a9dd0ec74.cfd/"):
        self.base_url = base_url.rstrip("/")
        # Paylaştığınız tarayıcı çıktısındaki header ve güvenlik parametrelerinin birebir aynısı
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36",
            "Referer": "https://taraftarium1089.xyz/",
            "Origin": "https://taraftarium1089.xyz/",
            "Accept": "*/*",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }

    def check_stream(self, channel_id="ss"):
        stream_url = f"{self.base_url}/{channel_id}/mono.m3u8"
        print(f"[*] İstek atılıyor: {stream_url}")
        
        try:
            response = requests.get(stream_url, headers=self.headers, timeout=10)
            
            print(f"[*] Durum Kodu: {response.status_code}")
            print(f"[*] Content-Type: {response.headers.get('Content-Type')}")
            print(f"[*] CF-Cache-Status: {response.headers.get('cf-cache-status')}")
            
            if response.status_code == 200:
                print("[+] Başarılı! Akış içeriği (ilk 300 karakter):")
                print("-" * 40)
                print(response.text[:300])
                print("-" * 40)
                return True
            else:
                print(f"[-] Hata Durum Kodu: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[!] Bağlantı Hatası: {str(e)}")
            return False

if __name__ == "__main__":
    scraper = TaraftariumProxyScraper("https://g1b.d72577a9dd0ec74.cfd/")
    scraper.check_stream("ss")
