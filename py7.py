import matplotlib.pyplot as plt

# Harf koordinatlarini tanimlayalim
# X ve Y eksenlerini 0-4095 araliginda daha iyi kullanacak sekilde genisletelim
# S harfini daha duzgun yapalim
atlas_coords_v2 = {
    'A1': [
        (200, 100), (400, 3995), (600, 100), (200, 100), # Sol taraf A
        (300, 2000), (500, 2000) # Yatay cizgi
    ],
    'T': [
        (800, 3995), (1200, 3995), (1000, 3995), # Yatay cizgi
        (1000, 100) # Dikey cizgi
    ],
    'L': [
        (1400, 3995), (1400, 100), # Dikey cizgi
        (1800, 100) # Yatay cizgi
    ],
    'A2': [
        (2000, 100), (2200, 3995), (2400, 100), (2000, 100), # Sag taraf A
        (2100, 2000), (2300, 2000) # Yatay cizgi
    ],
    'S': [
        (3200, 3500), # Baslangic (ust sag)
        (3000, 3995), # Ust sol kavis
        (2800, 3500), # Orta sol
        (3000, 2500), # Orta sag kavis
        (3200, 1500), # Alt sag
        (3000, 100),  # Alt sol kavis
        (2800, 500)   # Bitis (alt sol)
    ]
}

# Tüm koordinatları birleştirelim
all_coords_v2 = []
for letter in ['A1', 'T', 'L', 'A2', 'S']:
    all_coords_v2.extend(atlas_coords_v2[letter])

# Koordinatları yazdıralım
print("ATLAS yazısı için Güncellenmiş DAC Koordinatları (X, Y):")
for x, y in all_coords_v2:
    print(f"({x}, {y})")

# Koordinatları görselleştirelim
x_coords_v2, y_coords_v2 = zip(*all_coords_v2)

plt.figure(figsize=(12, 6)) # Boyutlari genisletelim
plt.plot(x_coords_v2, y_coords_v2, 'o-', markersize=4)
plt.title('ATLAS Galvo Scanner Path (Guncellenmis)')
plt.xlabel('X DAC Degeri')
plt.ylabel('Y DAC Degeri')
plt.xlim(0, 4095)
plt.ylim(0, 4095)
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('atlas_path_v2.png')