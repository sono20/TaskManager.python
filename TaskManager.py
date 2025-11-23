import json
import os
from datetime import datetime


class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Wczytuje zadania z pliku JSON"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        """Zapisuje zadania do pliku JSON"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, title, description=''):
        """Dodaje nowe zadanie"""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Dodano zadanie: {title}")

    def list_tasks(self, show_all=True):
        """Wyświetla listę zadań"""
        if not self.tasks:
            print("Brak zadań na liście.")
            return

        print("\n" + "=" * 60)
        print("LISTA ZADAŃ".center(60))
        print("=" * 60)

        for task in self.tasks:
            if show_all or not task['completed']:
                status = "✓" if task['completed'] else "○"
                print(f"\n[{task['id']}] {status} {task['title']}")
                if task['description']:
                    print(f"    Opis: {task['description']}")
                print(f"    Utworzono: {task['created_at']}")
        print("=" * 60)

    def complete_task(self, task_id):
        """Oznacza zadanie jako ukończone"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Zadanie '{task['title']}' oznaczone jako ukończone!")
                return
        print(f"✗ Nie znaleziono zadania o ID: {task_id}")

    def delete_task(self, task_id):
        """Usuwa zadanie"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Usunięto zadanie: {deleted_task['title']}")
                return
        print(f"✗ Nie znaleziono zadania o ID: {task_id}")

    def get_statistics(self):
        """Wyświetla statystyki zadań"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed

        print("\n" + "=" * 60)
        print("STATYSTYKI".center(60))
        print("=" * 60)
        print(f"Wszystkie zadania: {total}")
        print(f"Ukończone: {completed}")
        print(f"Do zrobienia: {pending}")
        if total > 0:
            print(f"Procent ukończenia: {(completed / total) * 100:.1f}%")
        print("=" * 60)


def main():
    manager = TaskManager()

    while True:
        print("\n--- MENEDŻER ZADAŃ ---")
        print("1. Dodaj zadanie")
        print("2. Pokaż wszystkie zadania")
        print("3. Pokaż zadania do zrobienia")
        print("4. Oznacz zadanie jako ukończone")
        print("5. Usuń zadanie")
        print("6. Statystyki")
        print("7. Wyjście")

        choice = input("\nWybierz opcję (1-7): ").strip()

        if choice == '1':
            title = input("Tytuł zadania: ").strip()
            if title:
                description = input("Opis (opcjonalnie): ").strip()
                manager.add_task(title, description)
            else:
                print("✗ Tytuł nie może być pusty!")

        elif choice == '2':
            manager.list_tasks(show_all=True)

        elif choice == '3':
            manager.list_tasks(show_all=False)

        elif choice == '4':
            manager.list_tasks(show_all=False)
            try:
                task_id = int(input("\nPodaj ID zadania do ukończenia: "))
                manager.complete_task(task_id)
            except ValueError:
                print("✗ Nieprawidłowe ID!")

        elif choice == '5':
            manager.list_tasks(show_all=True)
            try:
                task_id = int(input("\nPodaj ID zadania do usunięcia: "))
                manager.delete_task(task_id)
            except ValueError:
                print("✗ Nieprawidłowe ID!")

        elif choice == '6':
            manager.get_statistics()

        elif choice == '7':
            print("Do widzenia!")
            break

        else:
            print("✗ Nieprawidłowa opcja. Wybierz 1-7.")


if __name__ == "__main__":
    main()