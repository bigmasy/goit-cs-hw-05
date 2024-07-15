import asyncio
import aiofiles
import os
import argparse
from pathlib import Path

# Функція для обробки аргументів командного рядка
def parse_arguments():
    parser = argparse.ArgumentParser(description='Sort files by extension asynchronously')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('output_folder', type=str, help='Path to the output folder')
    return parser.parse_args()

# Асинхронна функція для читання файлів у вихідній папці
async def read_folder(source_folder, output_folder):
    tasks = []
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = Path(root) / file
            tasks.append(copy_file(source_path, output_folder))
    await asyncio.gather(*tasks)

# Асинхронна функція для копіювання файлів у відповідні підпапки
async def copy_file(source_path, output_folder):
    extension = source_path.suffix[1:]  # Отримання розширення файлу без точки
    if not extension:  # Пропустити файли без розширення
        return

    destination_folder = Path(output_folder) / extension
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_path = destination_folder / source_path.name

    try:
        async with aiofiles.open(source_path, 'rb') as src_file:
            content = await src_file.read()
        
        # Перевірка, чи існує файл у цільовій папці
        if destination_path.exists():
            print(f'File {destination_path} already exists. Skipping.')
            return

        async with aiofiles.open(destination_path, 'wb') as dst_file:
            await dst_file.write(content)
        print(f'Copied {source_path} to {destination_path}')
    except Exception as e:
        print(f'Error copying {source_path} to {destination_path}: {e}')

# Головна асинхронна функція
async def main():
    args = parse_arguments()
    source_folder = args.source_folder
    output_folder = args.output_folder

    await read_folder(source_folder, output_folder)

# Запуск головної функції
if __name__ == '__main__':
    asyncio.run(main())
