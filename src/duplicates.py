from collections import defaultdict

def find_and_save_duplicates(db):
    print("\n=== Поиск дубликатов ===")
    files = db.get_all_files()
    groups = defaultdict(list)
    for f in files:
        if f[5]:
            groups[f[5]].append(f)
    found = 0
    for h, flist in groups.items():
        if len(flist) > 1:
            found += 1
            print(f"Хеш: {h[:16]}... ({len(flist)} файлов)")
            for item in flist[:5]:
                print(f"  {item[1]} ({item[3]} байт)")
            if len(flist) > 5:
                print(f"  ... и ещё {len(flist)-5}")
            print()
    if found == 0:
        print("Дубликатов не найдено")
    else:
        print(f"Найдено групп дубликатов: {found}")