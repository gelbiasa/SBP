# INFORMASI:

# Sebelum melakukan Running saya mendownload tablutate terlebih dahulu  agar dapat melakukan running dengan tampilan tabel
# Hal yang perlu dilakukan, jika menggunakan windows buka Command Prompt atau PowerShell, sedangkan jika menggunakan MacOS atau linux buka terminal.
# Kemudian jalankan perintah "pip install tabulate"

from tabulate import tabulate

print("\n|=======================================================================================================================================================================================|")
print("\n|\t\t\t\t\t\t\t\tSaya mengambil data dari Jobsheet Pertemuan 11 'Contoh Kasus'\t\t\t\t\t\t\t\t|\n")
print("|=======================================================================================================================================================================================|\n")

# Data
data = [
    ["Kode", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
    ["A1", 1.10, 3.12, 3.89, 4.20, 2.21, 1.03, 3.00, 5.00],
    ["A2", 3.05, 3.98, 2.96, 3.02, 4.10, 2.99, 1.10, 4.03],
    ["A3", 1.90, 4.95, 3.01, 2.90, 4.95, 4.06, 5.00, 1.10],
    ["A4", 2.85, 3.87, 3.12, 1.05, 2.93, 4.89, 3.30, 4.90],
    ["A5", 4.77, 3.00, 4.87, 3.01, 1.97, 3.99, 2.04, 4.00]
]

# Bobot
bobot = [
    ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"],
    [0.178, 0.284, 0.207, 0.100, 0.057, 0.064, 0.044, 0.066]
]

# Tahap 1: Pembentukan matriks keputusan (X)
print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\t\tTahap 1: Pembentukan matriks keputusan (X)\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
print(tabulate(data, headers="firstrow", tablefmt="grid"))
print()

# Tahap 2: Normalisasi matriks keputusan (X)
min_values = [min(row[i] for row in data[1:]) for i in range(1, len(data[0]))]
max_values = [max(row[i] for row in data[1:]) for i in range(1, len(data[0]))]

normalized_data = [data[0]]  # header tetap sama
for row in data[1:]:
    normalized_row = [row[0]] + [(row[i] - min_values[i - 1]) / (max_values[i - 1] - min_values[i - 1]) for i in range(1, len(row))]
    normalized_data.append(normalized_row)

print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\tTahap 2: Matriks Keputusan (X) Setelah Normalisasi:\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
print(tabulate(normalized_data, headers="firstrow", tablefmt="grid"))
print()

# Tahap 3: Perhitungan elemen matriks tertimbang (V)
weighted_matrix = [data[0]]  # header tetap sama
for row in normalized_data[1:]:
    weighted_row = [row[0]] + [row[i] * bobot[1][i-1] + bobot[1][i-1] for i in range(1, len(row))]
    weighted_matrix.append(weighted_row)

print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\tTahap 3: Perhitungan Elemen Matriks Tertimbang (V):\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
print(tabulate(weighted_matrix, headers="firstrow", tablefmt="grid"))
print()

# Tahap 4: Matriks Area Perkiraan Batas (G)
G = ["G"]
for i in range(1, len(weighted_matrix[0])):
    column_values = [row[i] for row in weighted_matrix[1:]]
    product = 1
    for value in column_values:
        product *= value
    G.append(product ** (1/5))

print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\t\tTahap 4: Matriks Area Perkiraan Batas (G):\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
G_matrix = [["", *weighted_matrix[0][1:]], G]
print(tabulate(G_matrix, tablefmt="grid"))
print()

# Tahap 5: Perhitungan matriks jarak elemen alternatif dari batas perkiraan daerah (Q)
# Perhitungan Q menggunakan rumus: Q = V - G

Q = [["Alternatif"] + weighted_matrix[0][1:]]  # Header for the Q matrix

# Calculate Q for each alternative
for i in range(1, len(weighted_matrix)):
    Q_row = [weighted_matrix[i][0]]  # Alternative ID
    for j in range(1, len(weighted_matrix[i])):
        Q_value = weighted_matrix[i][j] - G[j]
        Q_row.append(Q_value)
    Q.append(Q_row)

print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\t\t\tTahap 5: Matriks Jarak (Q):\t\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
print(tabulate(Q, headers="firstrow", tablefmt="grid"))
print()

# Tahap 6: Perangkingan alternatif
ranking_scores = {}  # Dictionary to store the ranking scores for each alternative

# Calculate the sum for each alternative
for row in Q[1:]:
    alternative = row[0]
    score = sum(row[1:])  # Summing up all values except the first one (alternative ID)
    ranking_scores[alternative] = score

# Print the ranking scores
print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\t\t\tTahap 6: Perangkingan Alternatif\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
ranking_table = [[alternative, score] for alternative, score in ranking_scores.items()]
print(tabulate(ranking_table, headers=["Alternatif", "Skor"], tablefmt="grid"))

# Sort the ranking scores in ascending order
sorted_ranking = sorted(ranking_scores.items(), key=lambda x: x[1])

# Print the sorted ranking
print("|=======================================================================================================================================================================================|")
print("|\t\t\t\t\t\t\t\t\t\t\tPeringkat Alternatif:\t\t\t\t\t\t\t\t\t\t|")
print("|=======================================================================================================================================================================================|")
sorted_ranking_table = [[rank, alternative, score] for rank, (alternative, score) in enumerate(sorted_ranking, start=1)]
print(tabulate(sorted_ranking_table, headers=["Peringkat", "Alternatif", "Skor"], tablefmt="grid"))
