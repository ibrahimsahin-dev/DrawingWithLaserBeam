import tkinter as tk
import math

# --- AYARLAR ---
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
MAX_DAC_VALUE = 4095.0
LINE_COLOR = "black"
LINE_WIDTH = 2

# === YENİ EKLENEN AYAR ===
# Daha az koordinat almak için bu değeri ARTIRIN (örn: 20, 30)
# Daha çok koordinat almak için bu değeri AZALTIN (örn: 5, 2)
MIN_DISTANCE = 7  # Yeni bir noktanın kaydedilmesi için gereken minimum piksel mesafesi

# Global değişkenler
pixel_coordinates = [] 
last_x, last_y = None, None
last_recorded_x, last_recorded_y = None, None # Sadece kaydedilen son noktayı takip eder

# --- FONKSİYONLAR ---

def start_drawing(event):
    """Fare tuşuna basıldığında çizimi başlatır ve ilk noktayı kaydeder."""
    global last_x, last_y, last_recorded_x, last_recorded_y
    
    # Her yeni çizgi başladığında ilk noktayı kaydet
    pixel_coordinates.append((event.x, event.y))
    last_x, last_y = event.x, event.y
    last_recorded_x, last_recorded_y = event.x, event.y

def draw(event):
    """Fare hareket ettikçe çizim yapar ama sadece yeterli mesafe varsa kaydeder."""
    global last_x, last_y, last_recorded_x, last_recorded_y
    
    if last_x is not None:
        # Tuvale anlık olarak görünmesi için çizgi çiz (bu kısım her zaman çalışır)
        canvas.create_line(last_x, last_y, event.x, event.y, 
                           fill=LINE_COLOR, width=LINE_WIDTH, capstyle=tk.ROUND, smooth=tk.TRUE)
        last_x, last_y = event.x, event.y

        # === DEĞİŞTİRİLEN KISIM: MESAFE KONTROLÜ ===
        if last_recorded_x is not None:
            dist = math.sqrt((event.x - last_recorded_x)**2 + (event.y - last_recorded_y)**2)
            
            # Eğer mesafe eşik değerini aştıysa, yeni noktayı kaydet
            if dist >= MIN_DISTANCE:
                pixel_coordinates.append((event.x, event.y))
                last_recorded_x, last_recorded_y = event.x, event.y

def stop_drawing(event):
    """Fare tuşu bırakıldığında çizimi durdurur ve son noktayı kaydeder."""
    global last_x, last_y, last_recorded_x, last_recorded_y
    
    # Çizginin bittiği yeri de eklediğimizden emin olalım
    if last_x is not None and (last_x, last_y) not in pixel_coordinates:
         pixel_coordinates.append((last_x, last_y))

    # Kalem kalktı olarak işaretle
    pixel_coordinates.append(None) 
    last_x, last_y = None, None
    last_recorded_x, last_recorded_y = None, None


def clear_canvas():
    """Tuvali ve koordinat listesini temizler."""
    global pixel_coordinates
    canvas.delete("all")
    pixel_coordinates = []
    print("Tuval temizlendi.")

def export_coordinates():
    """Koordinatları ölçekler, terminale yazdırır ve dosyaya kaydeder."""
    if not pixel_coordinates:
        print("Çıktı alınacak koordinat bulunamadı. Lütfen önce çizim yapın.")
        return

    # "None" içermeyen temiz bir liste oluşturalım
    final_points = [p for p in pixel_coordinates if p is not None]

    if not final_points:
        print("Çıktı alınacak koordinat bulunamadı.")
        return

    scaled_x = []
    scaled_y = []

    print(f"\n--- {len(final_points)} ADET KOORDİNAT (0-4095) ---")
    
    for point in final_points:
        x = int((point[0] / CANVAS_WIDTH) * MAX_DAC_VALUE)
        y = int((point[1] / CANVAS_HEIGHT) * MAX_DAC_VALUE)
        y = int(MAX_DAC_VALUE - y)
        
        scaled_x.append(x)
        scaled_y.append(y)

    print("\nX Koordinatları:")
    print(scaled_x)
    print("\nY Koordinatları:")
    print(scaled_y)

    try:
        with open("cizim_koordinatlari_azaltilmis.txt", "w") as f:
            f.write(f"# Sizin Çiziminizden Oluşturulan {len(final_points)} Adet Koordinat\n\n")
            f.write("# X Koordinatları\n")
            f.write(str(scaled_x))
            f.write("\n\n# Y Koordinatları\n")
            f.write(str(scaled_y))
        print("\nKoordinatlar başarıyla 'cizim_koordinatlari_azaltilmis.txt' dosyasına kaydedildi.")
    except Exception as e:
        print(f"\nDosyaya yazarken bir hata oluştu: {e}")


# --- ARAYÜZ KURULUMU (DEĞİŞİKLİK YOK) ---
root = tk.Tk()
root.title("Azaltılmış Koordinat Çizici (0-4095)")
info_label = tk.Label(root, text="Fare ile beyaz alana çizin. Bitince 'Koordinatları Al' butonuna basın.", pady=10)
info_label.pack()
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", cursor="cross")
canvas.pack()
button_frame = tk.Frame(root, pady=10)
button_frame.pack()
export_button = tk.Button(button_frame, text="Koordinatları Al", command=export_coordinates, width=20, height=2)
export_button.pack(side=tk.LEFT, padx=10)
clear_button = tk.Button(button_frame, text="Temizle", command=clear_canvas, width=20, height=2)
clear_button.pack(side=tk.LEFT, padx=10)
canvas.bind("<ButtonPress-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)
root.mainloop()