import cv2
import numpy as np

def oku_koordinatlarini_kaydet(resim_yolu, cikti_dosya_yolu='koordinatlar.txt'):
    """
    Okun kontur noktalarının x ve y koordinatlarını bir metin dosyasına kaydeder.
    """
    # Resmi yükle
    resim = cv2.imread(resim_yolu)
    if resim is None:
        print("Hata: Resim bulunamadı.")
        return

    # Gri tonlamaya ve eşiklemeye dönüştür
    gri_resim = cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)
    _, esiklenmis_resim = cv2.threshold(gri_resim, 200, 255, cv2.THRESH_BINARY_INV)

    # Konturları bul
    konturlar, _ = cv2.findContours(esiklenmis_resim, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if konturlar:
        # En büyük konturu (oku) seç
        en_buyuk_kontur = max(konturlar, key=cv2.contourArea)

        if cv2.contourArea(en_buyuk_kontur) > 100:
            # Kontur noktalarını tek bir diziye sıkıştır
            kontur_noktalari = en_buyuk_kontur.squeeze()

            # x ve y koordinatlarını ayır
            x_koordinatlari = [nokta[0] for nokta in kontur_noktalari]
            y_koordinatlari = [nokta[1] for nokta in kontur_noktalari]
            
            # Koordinatları txt dosyasına yaz
            with open(cikti_dosya_yolu, 'w') as f:
                # x[] listesini yaz
                f.write("x[] = {")
                f.write(", ".join(map(str, x_koordinatlari)))
                f.write("};\n")
                
                # y[] listesini yaz
                f.write("y[] = {")
                f.write(", ".join(map(str, y_koordinatlari)))
                f.write("};\n")
            
            print(f"Koordinatlar '{cikti_dosya_yolu}' dosyasına başarıyla kaydedildi.")
        else:
            print("Ok tespit edilemedi veya çok küçük.")
    else:
        print("Resimde bir ok bulunamadı.")

# --- Kodu çalıştır ---
ok_resim_yolu = 'ok.png'
oku_koordinatlarini_kaydet(ok_resim_yolu)