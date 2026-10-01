# AWS Certified Solutions Architect - Associate (SAA-C03)

Espacio de estudio y base de conocimiento para la preparación del examen **AWS Certified Solutions Architect - Associate (SAA-C03)**.

---

## 📌 Acceso a los Apuntes

- **Map of Content (MOC):** [00_MOC_SAA-C03](./spanish/00_MOC_SAA-C03.md) — Índice maestro estructurado por dominios técnicos con enlaces bidireccionales para Obsidian.
- **Bóveda de Módulos:** [`spanish/Knowledge_Base/`](./spanish/Knowledge_Base/) — Contiene los 29 temas desarrollados con teoría técnica profunda, tablas y diagramas integrados.

---

## 🛠️ Herramientas de Extracción

El pipeline de extracción centralizado se encuentra en la raíz del repositorio (`../extractor.py`) y puede usarse de forma interactiva para cualquier curso y certificación:

- [`extractor.py`](../extractor.py): Script CLI en Python para procesar PDFs, extraer diapositivas como imágenes, limpiar marcas de agua y formatear Markdown compatible con Obsidian.

### Ejemplo de uso interactivo o por parámetros:
```bash
# Modo interactivo (solicita PDF, carpeta destino y archivo de secciones):
python ../extractor.py

# O especificando argumentos directos:
python ../extractor.py --pdf "ruta/al/curso.pdf" --config "ruta/al/_secciones_curso.txt" --output spanish/Knowledge_Base
```

> **Nota sobre archivos de secciones:** Los archivos auxiliares de mapeo de diapositivas del curso origen (por ejemplo `_secciones_solutions_architect.txt`) llevan el prefijo `_secciones` y están excluidos en `.gitignore` para no contaminar el historial del repositorio, ya que sólo sirven de apoyo temporal durante la extracción.
