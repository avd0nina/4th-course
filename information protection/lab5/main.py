from __future__ import annotations

import argparse
import struct
from pathlib import Path

# Смещения полей внутри заголовка BMP
HEADER_SIZE_FIELD_OFFSET = 10
DIB_SIZE_OFFSET = 14
WIDTH_OFFSET = 18
HEIGHT_OFFSET = 22
PLANES_OFFSET = 26
BPP_OFFSET = 28
COMPRESSION_OFFSET = 30
PIXEL_DATA_OFFSET = 54
MESSAGE_LENGTH_SIZE = 4

def _read_bmp(path: Path) -> tuple[bytearray, int]:
    # Читаем весь файл в изменяемый массив байтов: при внедрении
    # отдельные байты пикселей будут изменяться прямо в памяти
    data = bytearray(path.read_bytes())
    # Сигнатура "BM" в первых двух байтах подтверждает, что это BMP
    if len(data) < PIXEL_DATA_OFFSET or data[:2] != b"BM":
        raise ValueError("Файл не является BMP-изображением")
    # Получаем из заголовка параметры, необходимые для работы с пикселями
    pixel_offset = struct.unpack_from("<I", data, HEADER_SIZE_FIELD_OFFSET)[0]
    dib_size = struct.unpack_from("<I", data, DIB_SIZE_OFFSET)[0]
    width = struct.unpack_from("<i", data, WIDTH_OFFSET)[0]
    height = struct.unpack_from("<i", data, HEIGHT_OFFSET)[0]
    planes = struct.unpack_from("<H", data, PLANES_OFFSET)[0]
    bits_per_pixel = struct.unpack_from("<H", data, BPP_OFFSET)[0]
    compression = struct.unpack_from("<I", data, COMPRESSION_OFFSET)[0]
    # Проверяем, что формат изображения поддерживается программой
    if dib_size < 40:
        raise ValueError("Поддерживается BMP с заголовком BITMAPINFOHEADER")
    if width <= 0 or height == 0:
        raise ValueError("Некорректные размеры BMP-изображения")
    if planes != 1 or bits_per_pixel != 24 or compression != 0:
        raise ValueError(
            "Поддерживается только несжатое 24-битное цветное BMP-изображение"
        )
    if pixel_offset >= len(data):
        raise ValueError("Поврежденный BMP: некорректное смещение пикселей")
    # В BMP каждая строка выравнивается до количества байтов, кратного 4
    row_size = ((width * 3 + 3) // 4) * 4
    expected_size = pixel_offset + row_size * abs(height)
    if expected_size > len(data):
        raise ValueError("Поврежденный BMP: данные пикселей обрезаны")
    return data, pixel_offset

def _pixel_byte_positions(data: bytearray, pixel_offset: int):
    # В 24-битном BMP один пиксель занимает три байта:
    # по одному байту для синего, зеленого и красного компонентов
    width = struct.unpack_from("<i", data, WIDTH_OFFSET)[0]
    height = abs(struct.unpack_from("<i", data, HEIGHT_OFFSET)[0])
    row_size = ((width * 3 + 3) // 4) * 4
    for row in range(height):
        row_start = pixel_offset + row * row_size
        # Padding в конце строки не является цветом, поэтому его пропускаем
        yield from range(row_start, row_start + width * 3)

def _set_lsb(data: bytearray, positions, bits: str) -> None:
    for position, bit in zip(positions, bits):
        # Обнуляем младший бит исходного байта и записываем бит сообщения
        data[position] = (data[position] & 0xFE) | int(bit)

def _read_lsb(data: bytearray, positions, count: int) -> str:
    # Операция AND с единицей оставляет только младший бит байта
    return "".join(str(data[position] & 1) for position in positions[:count])

def _bytes_to_bits(value: bytes) -> str:
    # Переводим каждый байт в восемь символов двоичной записи
    return "".join(f"{byte:08b}" for byte in value)

def _bits_to_bytes(bits: str) -> bytes:
    # Обратное преобразование: собираем двоичную строку по 8 бит в байты
    return bytes(
        int(bits[index : index + 8], 2) for index in range(0, len(bits), 8)
    )

def embed(input_path: Path, output_path: Path, message: str) -> None:
    # Внедряет текстовое сообщение в копию BMP-файла
    data, pixel_offset = _read_bmp(input_path)
    positions = list(_pixel_byte_positions(data, pixel_offset))
    # Русский текст преобразуется в байты UTF-8 перед внедрением
    payload = message.encode("utf-8")
    # Первые 32 бита хранят длину сообщения, остальные - само сообщение
    payload_bits = _bytes_to_bits(struct.pack("<I", len(payload)) + payload)
    # Каждый цветовой байт хранит один бит, поэтому проверяем вместимость
    if len(payload_bits) > len(positions):
        capacity = (len(positions) - 32) // 8
        raise ValueError(
            f"Сообщение слишком большое. Максимальный размер: {capacity} байт"
        )
    _set_lsb(data, positions, payload_bits)
    output_path.write_bytes(data)

def extract(input_path: Path) -> str:
    # Извлекает текстовое сообщение из BMP-файла
    data, pixel_offset = _read_bmp(input_path)
    positions = list(_pixel_byte_positions(data, pixel_offset))
    if len(positions) < 32:
        raise ValueError("Изображение слишком маленькое для извлечения сообщения")
    # Сначала извлекаем 32 бита длины, чтобы определить,
    # сколько следующих битов относится к сообщению
    length_bits = _read_lsb(data, positions, 32)
    message_length = struct.unpack("<I", _bits_to_bytes(length_bits))[0]
    max_length = (len(positions) - 32) // 8
    if message_length > max_length:
        raise ValueError(
            "В изображении не найдено корректное внедренное сообщение"
        )
    # После длины считываем указанное количество бит самого сообщения
    message_bits = _read_lsb(data, positions[32:], message_length * 8)
    try:
        return _bits_to_bytes(message_bits).decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("Внедренное сообщение не является UTF-8-текстом") from error

def main() -> None:
    # Команда embed внедряет сообщение, а команда extract извлекает его
    parser = argparse.ArgumentParser(
        description="Внедрение и извлечение текста методом LSB-replacement"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    embed_parser = subparsers.add_parser("embed", help="внедрить сообщение в BMP")
    embed_parser.add_argument("input", type=Path, help="исходное BMP")
    embed_parser.add_argument("output", type=Path, help="BMP с сообщением")
    embed_parser.add_argument("message", help="сообщение для внедрения")
    extract_parser = subparsers.add_parser(
        "extract", help="извлечь сообщение из BMP"
    )
    extract_parser.add_argument("input", type=Path, help="BMP с сообщением")
    args = parser.parse_args()
    try:
        if args.command == "embed":
            embed(args.input, args.output, args.message)
            print(f"Сообщение внедрено: {args.output}")
        else:
            print(extract(args.input))
    except (OSError, ValueError) as error:
        # Ошибки файлов и некорректные BMP выводятся в понятном виде
        parser.error(str(error))

if __name__ == "__main__":
    main()
