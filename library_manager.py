import json
from dataclasses import dataclass
from typing import List

DATA_FILE = "library_storage.json"


@dataclass
class Book:
    """Класс, описывающий книгу"""

    id: int
    title: str
    author: str
    year: int
    status: str

    def to_dict(self) -> dict:
        """Преобразует книгу в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        """Создает обьект книги из словаря"""
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )

    def change_status(self, status: str) -> None:
        """Изменяет статус книги"""
        if status not in ["в наличии", "выдана"]:
            print("Недопустимый статус. Используйте 'в наличии' или 'выдана'.")
            return
        self.status = status
        print(f"Статус книги '{self.title}' изменён на '{status}'.")


@dataclass
class LibraryManager:
    """Класс для управления библиотекой"""

    data_file: str

    def _load_books(self) -> List[Book]:
        """Выгружаем все книги из библиотеки"""
        books = []
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                for line in file:
                    books.append(Book.from_dict(json.loads(line)))
        except FileNotFoundError:
            pass
        return books

    def _save_books(self, books: List[Book]) -> None:
        """Сохраняем книгу в файл"""
        with open(self.data_file, "w", encoding="utf-8") as file:
            for book in books:
                file.write(json.dumps(book.to_dict(), ensure_ascii=False) + "\n")

    def _generate_id(self) -> int:
        """Генерирует уникальный id для новой книги"""
        books = self._load_books()
        used_ids = {book.id for book in books}
        new_id = 1
        while new_id in used_ids:
            new_id += 1
        return new_id

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку"""
        new_book = Book(
            id=self._generate_id(),
            title=title,
            author=author,
            year=year,
            status="в наличии"
        )
        with open(self.data_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(new_book.to_dict(), ensure_ascii=False) + "\n")
        print(f"Книга '{title}' успешно добавлена")

    def delete_book(self, book_id: int) -> None:
        """Удаляет книгу по id"""
        books = self._load_books()
        updated_books = [book for book in books if book.id != book_id]

        if len(books) == len(updated_books):
            print(f"Книга с ID {book_id} не найдена")
            return

        self._save_books(updated_books)
        print(f"Книга с ID {book_id} успешно удалена")

    def find_books(self, keyword: str) -> List[Book]:
        """Ищет книги по названию, автору или году"""
        books = self._load_books()
        found_books = [
            book for book in books
            if keyword.lower() in book.title.lower()
               or keyword.lower() in book.author.lower()
               or keyword.isdigit() and int(keyword) == book.year
        ]
        return found_books

    def change_status(self, book_id: int, status: str) -> None:
        """Изменяет статус книги"""
        books = self._load_books()
        updated = False

        for book in books:
            if book.id == book_id:
                book.change_status(status)
                updated = True
                break

        if not updated:
            print(f"Книга с id {book_id} не найдена")
        else:
            self._save_books(books)

    def display_books(self) -> None:
        """Отображает все книги"""
        books = self._load_books()
        if not books:
            print("В библиотеке пока нет книг")
            return
        for book in books:
            print(
                f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")


def main():
    """Главная функция для запуска приложения"""
    manager = LibraryManager("library_storage.json")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            manager.add_book(title, author, year)

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            manager.delete_book(book_id)

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска: ")
            found_books = manager.find_books(keyword)
            if not found_books:
                print("Книги не найдены.")
            else:
                for book in found_books:
                    print(
                        f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")

        elif choice == "4":
            manager.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            manager.change_status(book_id, status)

        elif choice == "6":
            print("Выход из приложения. До свидания!")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ ==  "__main__":
    main()