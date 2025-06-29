import csv
import sys
import os

class User:
    """
    Reprezentuje użytkownika i jego dane o spożyciu wody.
    """
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.records = []  # lista wartości spożycia

    def add_record(self, amount):
        """Dodaje pojedynczy rekord spożycia (w litrach)."""
        try:
            value = float(amount)
            if value < 0:
                raise ValueError("Wartość spożycia nie może być ujemna")
            self.records.append(value)
        except ValueError as e:
            raise ValueError(f"Błąd dodawania rekordu dla użytkownika {self.user_id}: {e}")

    def average_consumption(self):
        """Zwraca średnie spożycie wody."""
        return sum(self.records) / len(self.records) if self.records else 0

class ConsumptionAnalyzer:
    """
    Analizuje i zarządza danymi spożycia wody dla wielu użytkowników.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.users = {}

    def load_data(self):
        """Wczytuje dane z pliku CSV. Oczekuje kolumn: user_id,name,amount"""
        if not os.path.exists(self.filepath):
            print(f"Plik '{self.filepath}' nie istnieje. Utworzony zostanie nowy przy zapisie.")
            return
        try:
            with open(self.filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user_id = row.get('user_id')
                    name = row.get('name')
                    amount = row.get('amount')

                    if not user_id or not name:
                        print(f"Pominięto niekompletny wiersz: {row}")
                        continue

                    if user_id not in self.users:
                        self.users[user_id] = User(user_id, name)
                    if amount:
                        try:
                            self.users[user_id].add_record(amount)
                        except ValueError as e:
                            print(e)
            print(f"Wczytano dane z '{self.filepath}'.")
        except csv.Error as e:
            print(f"Błąd odczytu pliku CSV: {e}")

    def save_data(self):
        """Zapisuje wszystkie rekordy do pliku CSV."""
        try:
            dirpath = os.path.dirname(self.filepath)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath)
            count = 0
            with open(self.filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['user_id', 'name', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for user in self.users.values():
                    for record in user.records:
                        writer.writerow({'user_id': user.user_id, 'name': user.name, 'amount': record})
                        count += 1
            abs_path = os.path.abspath(self.filepath)
            print(f"Zapisano {count} rekordów do pliku: {abs_path}")
        except OSError as e:
            print(f"Nie udało się zapisać danych do '{self.filepath}': {e}")

    def add_user(self, user_id, name):
        if user_id in self.users:
            print("Użytkownik o tym ID już istnieje.")
            return
        self.users[user_id] = User(user_id, name)
        print(f"Użytkownik '{name}' został dodany.")

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            print(f"Użytkownik o ID '{user_id}' usunięty.")
        else:
            print("Nie znaleziono użytkownika.")

    def update_user_name(self, user_id, new_name):
        user = self.users.get(user_id)
        if user:
            user.name = new_name
            print(f"Nazwa użytkownika o ID '{user_id}' zaktualizowana na '{new_name}'.")
        else:
            print("Nie znaleziono użytkownika.")

    def add_user_record(self, user_id, amount):
        user = self.users.get(user_id)
        if user:
            try:
                user.add_record(amount)
                print(f"Dodano rekord {amount} L dla użytkownika '{user.name}' (ID: {user_id}).")
            except ValueError as e:
                print(e)
        else:
            print("Nie znaleziono użytkownika.")

    def show_user_data(self, user_id):
        user = self.users.get(user_id)
        if user:
            print(f"\nDane użytkownika '{user.name}' (ID: {user.user_id}):")
            print(f"  Rekordy: {user.records}")
            print(f"  Średnie spożycie: {user.average_consumption():.2f} L\n")
        else:
            print("Nie znaleziono użytkownika.")

    def show_all_users(self):
        if not self.users:
            print("Brak użytkowników.")
            return
        print("\n==== Lista użytkowników ====")
        for user in self.users.values():
            avg = user.average_consumption()
            print(f"- ID: {user.user_id} | Imię: {user.name} | Średnie spożycie: {avg:.2f} L | Rekordy: {user.records}")
        print()


def display_menu():
    print("""
==== MENU ====
1. Dodaj użytkownika
2. Zmień nazwę użytkownika
3. Dodaj rekord spożycia
4. Wyświetl dane użytkownika
5. Usuń użytkownika
6. Zapisz dane i zakończ
7. Wyjście bez zapisu
8. Wyświetl wszystkich użytkowników
""")


def main():
    filepath = "C:/Users/piotr/Desktop/SkryptoweLaborki/Projekt/water_data.csv"
    analyzer = ConsumptionAnalyzer(filepath)
    analyzer.load_data()

    while True:
        display_menu()
        choice = input("Wybierz opcję: ").strip()

        if choice == '1':
            uid = input("Podaj ID użytkownika: ").strip()
            name = input("Podaj nazwę użytkownika: ").strip()
            analyzer.add_user(uid, name)
        elif choice == '2':
            uid = input("Podaj ID użytkownika: ").strip()
            new_name = input("Podaj nową nazwę: ").strip()
            analyzer.update_user_name(uid, new_name)
        elif choice == '3':
            uid = input("Podaj ID użytkownika: ").strip()
            amount = input("Podaj ilość spożycia (L): ").strip()
            analyzer.add_user_record(uid, amount)
        elif choice == '4':
            uid = input("Podaj ID użytkownika: ").strip()
            analyzer.show_user_data(uid)
        elif choice == '5':
            uid = input("Podaj ID użytkownika: ").strip()
            analyzer.remove_user(uid)
        elif choice == '6':
            analyzer.save_data()
            print("Zakończono.")
            break
        elif choice == '7':
            print("Zakończono bez zapisu.")
            break
        elif choice == '8':
            analyzer.show_all_users()
        else:
            print("Nieprawidłowa opcja.")

if __name__ == "__main__":
    main()
