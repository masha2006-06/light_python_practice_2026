def format_size(bytes):
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"

def print_report(db):
    print("=" * 40)
    print("ОТЧЕТ")
    print("=" * 40)
    print("Файлов:", db.get_files_count())
    print("Размер:", format_size(db.get_total_size()))
    print("=" * 40)