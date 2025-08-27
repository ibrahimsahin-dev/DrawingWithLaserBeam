import matplotlib.pyplot as plt

x = [101, 100, 236, 103, 99, 363, 109, 267, 265, 403, 265, 268, 527, 272, 433, 432, 567, 433, 435, 696, 441]
y = [152, 272, 400, 525, 649, 401, 159, 153, 273, 400, 527, 645, 403, 156, 151, 273, 401, 528, 652, 403, 157]

plt.figure(figsize=(10, 6))
plt.plot(x, y, '-o', linewidth=2)
plt.title('Noktaların Birleştirilmesiyle Oluşan Şekil')
plt.xlabel('X Koordinatı'); plt.ylabel('Y Koordinatı')
plt.grid(True); plt.axis('equal')
plt.show()