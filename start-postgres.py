import subprocess

# Путь к исполняемому файлу postgres.exe
postgres_path = "C:/Program Files/PostgreSQL/11/bin/postgres.exe"

# Аргументы для запуска сервера
args = [
    "-D", "C:/Program Files/PostgreSQL/11/data",
    "-p", "5432"
]

# Запуск сервера в отдельном процессе
subprocess.Popen([postgres_path] + args)
