import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv('transakcje.csv')
df['Data'] = pd.to_datetime(df['Data'])

print("=" * 60)
print("ANALIZA FINANSOWA - TRANSAKCJE STUDENCKIE")
print("=" * 60)

# Kategoryzacja transakcji
def kategoryzuj(opis, kwota):
    if kwota > 0:
        return 'Wpływy'

    opis = opis.lower()
    if any(sklep in opis for sklep in ['biedronka', 'lidl', 'kaufland', 'zahka', 'żabka']):
        return 'Zakupy spożywcze'
    elif any(slowo in opis for slowo in ['czynsz', 'prąd', 'media']):
        return 'Mieszkanie i media'
    elif any(slowo in opis for slowo in ['netflix', 'spotify']):
        return 'Subskrypcje'
    elif any(slowo in opis for slowo in ['mpk', 'uber', 'bolt', 'bilet']):
        return 'Transport'
    elif any(slowo in opis for slowo in ['bar', 'pizz', 'kebab', 'kfc', 'mcdonald', 'burger', 'restaur', 'sushi', 'pasta']):
        return 'Jedzenie na mieście'
    elif any(slowo in opis for slowo in ['kino', 'cinema', 'multikino', 'helios', 'sylwester']):
        return 'Rozrywka'
    elif any(slowo in opis for slowo in ['coffee', 'starbucks', 'costa', 'caffe']):
        return 'Kawiarnie'
    elif any(slowo in opis for slowo in ['rossmann', 'empik', 'reserved', 'h&m', 'prezent']):
        return 'Zakupy i inne'
    else:
        return 'Inne'

df['Kategoria'] = df.apply(lambda row: kategoryzuj(row['Opis_Transakcji'], row['Kwota']), axis=1)

# Suma dla każdej kategorii
print("\nSUMA WYDATKÓW DLA KAŻDEJ KATEGORII:")
print("-" * 60)
kategorie_suma = df.groupby('Kategoria')['Kwota'].sum().sort_values()
for kategoria, suma in kategorie_suma.items():
    if kategoria != 'Wpływy':
        print(f"{kategoria}: {suma:.2f} zł")

# Wykres kołowy - tylko wydatki (bez wpływów)
print("\nGenerowanie wykresu...")
wydatki_df = df[df['Kategoria'] != 'Wpływy']
kategorie_wydatki = wydatki_df.groupby('Kategoria')['Kwota'].sum().abs().sort_values(ascending=False)

plt.figure(figsize=(10, 8))
colors = plt.cm.Set3(range(len(kategorie_wydatki)))
plt.pie(kategorie_wydatki, labels=kategorie_wydatki.index, autopct='%1.1f%%',
        startangle=90, colors=colors)
plt.title('Struktura wydatków według kategorii', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('wydatki_wykres.png', dpi=300, bbox_inches='tight')
print("Zapisano wykres: wydatki_wykres.png")

# Podsumowanie końcowe
print("\n" + "=" * 60)
print("PODSUMOWANIE FINANSOWE")
print("=" * 60)

wplywy = df[df['Kwota'] > 0]['Kwota'].sum()
wydatki = df[df['Kwota'] < 0]['Kwota'].sum()
bilans = wplywy + wydatki

print(f"\nŁącznie wydano:  {abs(wydatki):,.2f} zł")
print(f"Łącznie wpłynęło: {wplywy:,.2f} zł")
print(f"Bilans:           {bilans:,.2f} zł")
print("\n" + "=" * 60)
