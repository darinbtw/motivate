def delete_line_from_file(file_path, line_number):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Убедиться, что номер строки в допустимом диапазоне
        if 0 <= line_number < len(lines):
            del lines[line_number]
        else:
            print("Неверный номер строки.")
            return
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        
        print(f"Строка {line_number + 1} удалена.")
    
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
file_path = 'example.txt'
line_number = 0  # Номер строки для удаления (нумерация с нуля)
delete_line_from_file(file_path, line_number)
