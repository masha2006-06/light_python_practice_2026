import os
import hashlib
from datetime import datetime
from pathlib import Path

def scan_folder(path, db, extensions=None):
    root = Path(path)
    if not root.exists():
        print("Ошибка: путь не существует")
        return 0

    count = 0
    total_size = 0
    print("Сканирование...")

    def _walk_dir(current_path):
        nonlocal count, total_size
        for item in current_path.iterdir():
            if item.is_file():
                if extensions is not None and item.suffix not in extensions:
                    continue
                try:
                    stat = item.stat()
                    hash_val = calc_hash(item)
                    db.save_file(
                        str(item),
                        item.name,
                        stat.st_size,
                        datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        hash_val,
                        str(item.parent)
                    )
                    count += 1
                    total_size += stat.st_size
                    if count % 100 == 0:
                        print(f"  Обработано {count} файлов")
                except Exception as e:
                    print(f"  Ошибка при обработке {item}: {e}")
            elif item.is_dir():
                _walk_dir(item)

    _walk_dir(root)
    print(f"Готово! Файлов: {count}, общий размер: {total_size} байт")
    db.save_scan_history(str(path), count, total_size)
    return count

def calc_hash(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None