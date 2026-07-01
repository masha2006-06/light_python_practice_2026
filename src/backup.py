import os
import hashlib
from pathlib import Path
from datetime import datetime

def compare_with_backup(original_path, backup_path, db):
    print("\n=== Сравнение с резервной копией ===")
    print(f"Оригинал: {original_path}")
    print(f"Резервная копия: {backup_path}")

    orig_info = collect_file_info(original_path)
    backup_info = collect_file_info(backup_path)

    missing = []
    changed = []
    extra = []

    for rel_path, info in orig_info.items():
        if rel_path not in backup_info:
            missing.append(rel_path)
        elif info['hash'] != backup_info[rel_path]['hash']:
            changed.append(rel_path)

    for rel_path in backup_info:
        if rel_path not in orig_info:
            extra.append(rel_path)

    print(f"Файлов в оригинале: {len(orig_info)}")
    print(f"Файлов в бэкапе: {len(backup_info)}")
    print(f"Отсутствуют в бэкапе: {len(missing)}")
    print(f"Изменены: {len(changed)}")
    print(f"Лишние в бэкапе: {len(extra)}")

    if missing:
        print("\n--- Отсутствуют в бэкапе ---")
        for f in missing[:10]:
            print(f"  {f}")
        if len(missing) > 10:
            print(f"  ... и ещё {len(missing)-10}")

    if changed:
        print("\n--- Изменены ---")
        for f in changed[:10]:
            print(f"  {f}")
        if len(changed) > 10:
            print(f"  ... и ещё {len(changed)-10}")

    if extra:
        print("\n--- Лишние в бэкапе ---")
        for f in extra[:10]:
            print(f"  {f}")
        if len(extra) > 10:
            print(f"  ... и ещё {len(extra)-10}")

    db.save_backup_check(original_path, backup_path, missing, changed, extra)
    return missing, changed, extra

def collect_file_info(root_path):
    root = Path(root_path)
    if not root.exists():
        return {}
    info = {}
    for file_path in root.rglob('*'):
        if file_path.is_file():
            rel = str(file_path.relative_to(root))
            try:
                h = hashlib.md5()
                with open(file_path, 'rb') as f:
                    while chunk := f.read(8192):
                        h.update(chunk)
                info[rel] = {
                    'hash': h.hexdigest(),
                    'size': file_path.stat().st_size
                }
            except:
                pass
    return info