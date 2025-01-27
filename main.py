import subprocess
import os
import argparse
from tqdm import tqdm

def extract_rar(archive, password):
    rar_path = r"C:\Program Files\WinRAR\Rar.exe" # Замени, если отличается
    
    command = [rar_path, 'x', f'-p{password}', archive]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Брутфорс паролей для RAR-архивов.")
    parser.add_argument("archive", help="Имя RAR-архива")
    parser.add_argument("password_file", help="Текстовый файл с паролями")
    
    args = parser.parse_args()

    if not os.path.isfile(args.archive):
        print(f"Ошибка: Архив '{args.archive}' не найден.")
        return

    if not os.path.isfile(args.password_file):
        print(f"Ошибка: Файл '{args.password_file}' не найден.")
        return
    
    with open(args.password_file, 'r', encoding='utf-8') as f:
        passwords = f.readlines()
        
    progress_bar = tqdm(total=len(passwords), desc="Перебор паролей", unit=' pass', leave=False)

    for line in passwords:
        password = line.strip()
        if extract_rar(args.archive, password):
            progress_bar.close()
            print(f"\n[+] Пароль найден: {password}\n")
            return
        progress_bar.update(1)

    progress_bar.close()
    print("[-] Пароль не найден в файле.")

if __name__ == "__main__":
    main()