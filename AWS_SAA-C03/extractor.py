"""
extractor.py - Plantilla Genérica y Modular de Extracción de Cursos en PDF para Obsidian y Data Lake

Este script procesa diapositivas/documentos PDF de cualquier certificación o curso técnico:
1. Divide el PDF en módulos/secciones según un archivo o lista de configuración de secciones.
2. Limpia marcas de autoría, textos promocionales y marcas de agua de forma configurable vía Regex.
3. Extrae texto e imágenes vinculadas a cada slide optimizadas para visualización en Obsidian (Markdown + media).
4. Genera carpetas limpias y normalizadas (sin caracteres extraños o espacios conflictivos).
"""

import os
import re
import ast
import argparse
from pathlib import Path

import pymupdf


# ==========================================
# ⚙️ CONFIGURACIÓN POR DEFECTO
# ==========================================

# Patrones regex configurables para eliminar de las transcripciones crudas (autores, marcas, webs)
PATRONES_LIMPIEZA_DEFECTO = [
    r'(?i)©?\s*[A-Za-zÁ-ÿ\s]+(?:&|y|and)\s*[A-Za-zÁ-ÿ\s]+(?:LLC|Inc)?',  # Ejemplo de autores múltiples
    r'(?i)NOT\s+FOR\s+DISTRIBUTION',                                    # Advertencias de copyright
    r'(?i)www\.[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}',                       # URLs genéricas
]

# Ejemplo de estructura de secciones para pruebas rápidas
SECCIONES_EJEMPLO = [
    ("Introducción y Conceptos Básicos", 1, 10),
    ("Arquitectura y Componentes Clave", 11, 25),
    ("Prácticas Recomendadas y Conclusiones", 26, 40),
]


def sanitizar_nombre(nombre: str) -> str:
    """
    Sanitiza nombres de carpetas y archivos para que sean compatibles con todos los SO,
    Obsidian y sistemas de rutas web/git.
    Elimina caracteres problemáticos como &, paréntesis, comas y reemplaza espacios y guiones feos.
    """
    nombre = nombre.replace("&", "and")
    nombre = re.sub(r'[\(\)\[\]\{\}\<\>|\\/*?:\'\"`]', '', nombre)
    nombre = re.sub(r'[\s_]*[-–—]+[\s_]*', '_', nombre)
    nombre = re.sub(r'[,;.]', '', nombre)
    nombre = re.sub(r'\s+', '_', nombre)
    nombre = re.sub(r'_+', '_', nombre)
    return nombre.strip('_')


def limpiar_texto(texto: str, patrones_limpieza: list[str]) -> str:
    """
    Aplica una lista de reglas Regex para limpiar el texto extraído del PDF
    y normaliza los saltos de línea repetidos.
    """
    for patron in patrones_limpieza:
        texto = re.sub(patron, '', texto)
    
    # Reducir saltos de línea excesivos (máximo 2 consecutivos)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    return texto.strip()


def cargar_secciones_desde_archivo(ruta_archivo: Path) -> list[tuple[str, int, int]]:
    """
    Carga dinámicamente la lista de secciones desde un archivo .txt o .py.
    Permite el formato:
    SECCIONES = [
        ("Nombre Sección", pagina_inicio, pagina_fin),
        ...
    ]
    o simplemente listas de tuplas directas.
    """
    contenido = ruta_archivo.read_text(encoding="utf-8")
    
    # Buscar si contiene la variable SECCIONES = [...]
    match = re.search(r'SECCIONES\s*=\s*(\[[\s\S]*?\])', contenido)
    if match:
        bloque = match.group(1)
        return ast.literal_eval(bloque)
    
    # Si no tiene el prefijo, intentar evaluar el contenido como lista literal
    try:
        resultado = ast.literal_eval(contenido.strip())
        if isinstance(resultado, list):
            return resultado
    except Exception:
        pass
    
    raise ValueError(f"No se pudo parsear la lista SECCIONES en el archivo: {ruta_archivo}")


def extraer_curso(
    pdf_path: Path,
    output_dir: Path,
    secciones: list[tuple[str, int, int]],
    patrones_limpieza: list[str] = None,
    formato_obsidian: bool = True
):
    """
    Ejecuta el pipeline de extracción de texto e imágenes por sección.
    
    :param pdf_path: Ruta al archivo PDF original.
    :param output_dir: Directorio base de salida para las carpetas generadas.
    :param secciones: Lista de tuplas (titulo, pag_inicio, pag_fin) con base 1.
    :param patrones_limpieza: Expresiones regulares para suprimir firmas o marcas.
    :param formato_obsidian: Si True, formatea imágenes y títulos con compatibilidad Obsidian.
    """
    if patrones_limpieza is None:
        patrones_limpieza = PATRONES_LIMPIEZA_DEFECTO

    if not pdf_path.exists():
        raise FileNotFoundError(f"No se encontró el PDF en: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    total_paginas = doc.page_count
    print(f"📄 Abriendo documento: {pdf_path.name} ({total_paginas} páginas)")
    print(f"⚡ Procesando {len(secciones)} secciones configuradas...")

    output_dir.mkdir(parents=True, exist_ok=True)

    for i, (titulo_seccion, pag_inicio, pag_fin) in enumerate(secciones):
        inicio_idx = max(0, pag_inicio - 1)
        fin_idx = min(pag_fin, total_paginas)
        
        num_seccion = str(i + 1).zfill(2)
        nombre_limpio = sanitizar_nombre(titulo_seccion)
        nombre_carpeta = f"{num_seccion}_{nombre_limpio}"
        
        ruta_seccion = output_dir / nombre_carpeta
        ruta_media = ruta_seccion / "media"
        ruta_media.mkdir(parents=True, exist_ok=True)
        
        texto_seccion = f"# {titulo_seccion}\n\n"
        if formato_obsidian:
            texto_seccion = (
                f"---\n"
                f"modulo: \"{num_seccion}\"\n"
                f"tema: \"{titulo_seccion}\"\n"
                f"paginas: {pag_inicio}-{pag_fin}\n"
                f"---\n\n"
                f"# {titulo_seccion}\n\n"
            )

        imagenes_extraidas = 0

        for num_pag in range(inicio_idx, fin_idx):
            pagina = doc.load_page(num_pag)
            
            # --- Extracción y Limpieza de Texto ---
            texto_crudo = pagina.get_text("text")
            texto_limpio = limpiar_texto(texto_crudo, patrones_limpieza)
            
            if texto_limpio:
                texto_seccion += f"### Slide {num_pag + 1}\n{texto_limpio}\n\n"

            # --- Extracción de Imágenes de la Diapositiva ---
            for img_idx, img in enumerate(pagina.get_images(full=True)):
                xref = img[0]
                imagen_base = doc.extract_image(xref)
                bytes_imagen = imagen_base["image"]
                ext_imagen = imagen_base["ext"]
                
                nombre_imagen = f"slide{num_pag + 1}_img{img_idx + 1}.{ext_imagen}"
                ruta_imagen = ruta_media / nombre_imagen
                
                with open(ruta_imagen, "wb") as f_img:
                    f_img.write(bytes_imagen)
                
                imagenes_extraidas += 1
                
                if formato_obsidian:
                    texto_seccion += f"![{nombre_imagen}](./media/{nombre_imagen})\n\n"
                else:
                    texto_seccion += f"![[{nombre_imagen}]]\n\n"

        # Guardar archivo Markdown / Texto de la sección
        nombre_archivo = f"{nombre_limpio}.md" if formato_obsidian else "raw_text.txt"
        ruta_archivo = ruta_seccion / nombre_archivo
        ruta_archivo.write_text(texto_seccion, encoding="utf-8")

        print(f"  [+] Seccion {num_seccion}: {nombre_limpio} (pags {pag_inicio}-{pag_fin}) | {imagenes_extraidas} imgs")

    print("\n✅ ¡Extracción completada con éxito!")


def main():
    parser = argparse.ArgumentParser(description="Extractor de diapositivas PDF a Markdown optimizado para Obsidian.")
    parser.add_argument("--pdf", type=str, help="Ruta al archivo PDF a procesar.", default=None)
    parser.add_argument("--config", type=str, help="Archivo .txt o .py con la variable SECCIONES.", default=None)
    parser.add_argument("--output", type=str, help="Directorio destino.", default="Knowledge_Base")
    parser.add_argument("--autores", nargs="*", help="Nombres o frases adicionales a limpiar de los slides.", default=[])

    args = parser.parse_args()
    script_dir = Path(__file__).parent

    # Resolver PDF
    if args.pdf:
        pdf_path = Path(args.pdf)
    else:
        # Búsqueda automática de algún PDF en el directorio del script
        candidatos_pdf = list(script_dir.glob("*.pdf"))
        if candidatos_pdf:
            pdf_path = candidatos_pdf[0]
        else:
            pdf_path = script_dir / "curso.pdf"

    # Resolver Secciones
    if args.config:
        config_path = Path(args.config)
        secciones = cargar_secciones_desde_archivo(config_path)
    else:
        archivo_secciones = script_dir / "secciones_solutions_architect.txt"
        if archivo_secciones.exists():
            secciones = cargar_secciones_desde_archivo(archivo_secciones)
        else:
            print("⚠️ No se proporcionó archivo de secciones. Utilizando configuración de ejemplo...")
            secciones = SECCIONES_EJEMPLO

    # Configurar patrones de limpieza
    patrones = list(PATRONES_LIMPIEZA_DEFECTO)
    for autor in args.autores:
        patron_autor = rf'(?i){re.escape(autor)}'
        patrones.append(patron_autor)

    output_dir = Path(args.output) if args.output else (script_dir / "Knowledge_Base")

    extraer_curso(
        pdf_path=pdf_path,
        output_dir=output_dir,
        secciones=secciones,
        patrones_limpieza=patrones,
        formato_obsidian=True
    )


if __name__ == "__main__":
    main()