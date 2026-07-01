import sys
import os
import argparse
from database import Database
from scanner import scan_folder
from report import print_report
from duplicates import find_and_save_duplicates
from backup import compare_with_backup

def main():
    parser = argparse.ArgumentParser(description="Индексатор папок (полный вариант)")
    parser.add_argument("path", help="Путь к папке для индексации")
    parser.add_argument("--extensions", nargs="+", help="Фильтр по расширениям, например .py .txt")
    parser.add_argument("--find-duplicates", action="store_true", help="Найти дубликаты")
    parser.add_argument("--backup", help="Путь к папке с резервной копией для сравнения")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("Ошибка: путь не существует")
        sys.exit(1)

    db = Database("index.db")
    print("База данных готова")

    print(f"Индексация: {args.path}")
    scan_folder(args.path, db, extensions=args.extensions)

    print_report(db)

    if args.find_duplicates:
        find_and_save_duplicates(db)

    if args.backup:
        if not os.path.exists(args.backup):
            print(f"Ошибка: папка бэкапа '{args.backup}' не существует")
            sys.exit(1)
        compare_with_backup(args.path, args.backup, db)

if __name__ == "__main__":
    main()