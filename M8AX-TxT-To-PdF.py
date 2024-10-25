"""
Este Programa Convierte Archivos De Texto ( .txt, .py, .log, .csv, .xml, .json, .html, .md, .sql, .yaml, .ini, .cfg, .java, .c, .cpp, .rb, .sh, .bat ) A Archivos PDF.
El Usuario Debe Proporcionar Un Directorio De Entrada Conteniendo Los Archivos
A Convertir Y Un Directorio De Salida Donde Se Guardarán Los Archivos PDF Generados.

Funciones Principales:

1. Clear_Screen: Limpia La Pantalla De La Consola Antes De Iniciar El Programa.
2. Txt_To_Pdf: Convierte Un Archivo De Texto En Un Archivo PDF Utilizando La Fuente Arial.
3. Process_Directory: Procesa Todos Los Archivos En El Directorio De Entrada, Creando La Estructura
   De Carpetas Correspondiente En El Directorio De Salida Y Actualiza Una Barra De Progreso.

La Barra De Progreso Muestra El Progreso De La Conversión De Archivos, Y La Descripción
De La Barra Se Muestra En Color Amarillo Para Mejorar La Visibilidad.

Programador: MarcoS OchoA DieZ ( Alias: M8AX ) 
Fecha De Programación: 25 De Octubre De 2024 - Viernes - 00:00
Duración De Programación: 1.5h
Dispositivo Utilizado: MvIiIaX - Xiaomi MI 9 Lite ( TerMuX Con PyThoN ) 
Código Formateado Con: BlacK
"""

import os
import contextlib
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from fpdf import FPDF
from tqdm import tqdm


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def txt_to_pdf(txt_file, pdf_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", "arial.ttf")
    pdf.set_font("Arial", size=14)

    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().replace("\r\n", "\n").strip()
    except UnicodeDecodeError:
        with open(txt_file, "r", encoding="latin-1") as f:
            text = f.read().replace("\r\n", "\n").strip()

    lines = text.split("\n")
    for line in lines:
        if line.strip():
            pdf.multi_cell(0, 10, line)
            pdf.ln(1)

    pdf.output(pdf_file)


def process_file(file, input_dir, output_dir):
    rel_path = os.path.relpath(file, input_dir)
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(rel_path)[0]}.pdf")

    output_subdir = os.path.dirname(output_file_path)
    os.makedirs(output_subdir, exist_ok=True)

    with contextlib.redirect_stdout(open(os.devnull, "w")), contextlib.redirect_stderr(
        open(os.devnull, "w")
    ):
        txt_to_pdf(file, output_file_path)


def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = int(seconds % 60)
    return int(days), int(hours), int(minutes), int(seconds)


def process_directory(input_dir, output_dir, num_cores):
    files_to_convert = []

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(
                (
                    ".txt",
                    ".py",
                    ".log",
                    ".csv",
                    ".xml",
                    ".json",
                    ".html",
                    ".md",
                    ".sql",
                    ".yaml",
                    ".yml",
                    ".ini",
                    ".cfg",
                    ".java",
                    ".c",
                    ".cpp",
                    ".rb",
                    ".sh",
                    ".bat",
                )
            ):
                files_to_convert.append(os.path.join(root, file))

    start_time = time.time()
    num_files = len(files_to_convert)

    if num_files == 0:
        print("\nM8AX - No Se Encontraron Archivos Para Procesar.")
        return

    print("")

    with tqdm(
        total=num_files,
        desc="M8AX - Paso 1/1 - ",
        unit=" Archivo",
        leave=True,
        colour="Yellow",
    ) as pbar:
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            futures = {
                executor.submit(process_file, file, input_dir, output_dir): file
                for file in files_to_convert
            }
            for future in as_completed(futures):
                pbar.update(1)
                os.system("play -n synth 0.0050 sin 100 > /dev/null 2>&1")

    end_time = time.time()
    elapsed_time = end_time - start_time
    cores_used = num_cores
    files_per_second = num_files / elapsed_time if elapsed_time > 0 else 0

    days, hours, minutes, seconds = format_time(elapsed_time)
    print(
        f"\nM8AX - Tiempo De Proceso Total: {days} Días, {hours} Horas, {minutes} Minutos, Y {seconds} Segundos."
    )
    print(f"\nM8AX - Total De Ficheros Procesados: {num_files}.")
    print(f"\nM8AX - Ficheros Procesados Por Segundo: {files_per_second:.5f}.")
    print(f"\nM8AX - Número De Núcleos Usados: {cores_used}.\n")


def main():
    clear_screen()
    input_dir = input("M8AX - Introduce El Directorio De Entrada: ")
    while not os.path.exists(input_dir):
        print("\nM8AX - El Directorio No Existe. Por Favor, Inténtalo De Nuevo.")
        input_dir = input("\nM8AX - Introduce El Directorio De Entrada: ")
    output_dir = input("\nM8AX - Introduce El Directorio De Salida: ")

    available_cores = multiprocessing.cpu_count()

    while True:
        try:
            num_cores = int(
                input(
                    f"\nM8AX - Introduce El Número De Cores A Usar (1-{available_cores}): "
                )
            )
            if 1 <= num_cores <= available_cores:
                break
            else:
                print(
                    f"\nM8AX - Por Favor, Introduce Un Número Entre 1 Y {available_cores}."
                )
        except ValueError:
            print("\nM8AX - Por Favor, Introduce Un Número Válido.")

    os.makedirs(output_dir, exist_ok=True)
    process_directory(input_dir, output_dir, num_cores)


if __name__ == "__main__":
    main()