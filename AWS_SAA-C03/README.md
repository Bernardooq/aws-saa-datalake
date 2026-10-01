# AWS Certified Solutions Architect - Associate (SAA-C03)

Espacio de estudio y base de conocimiento para la preparación del examen **AWS Certified Solutions Architect - Associate (SAA-C03)**.

---

## 📌 Acceso a los Apuntes

- **Map of Content (MOC):** [00_MOC_SAA-C03](./spanish/00_MOC_SAA-C03.md) — Índice maestro estructurado por dominios técnicos con enlaces bidireccionales para Obsidian.
- **Bóveda de Módulos:** [`spanish/Knowledge_Base/`](./spanish/Knowledge_Base/) — Contiene los 29 temas desarrollados con teoría técnica profunda, tablas y diagramas integrados.

---

## 🛠️ Herramientas de Extracción

El directorio incluye scripts modulares para automatizar la extracción de nuevos materiales y diapositivas:

- [`extractor.py`](./extractor.py): Script CLI en Python para procesar PDFs, extraer diapositivas como imágenes, limpiar marcas de agua y formatear Markdown compatible con Obsidian.
- [`secciones_solutions_architect.txt`](./secciones_solutions_architect.txt): Definición de las 29 secciones con sus rangos de páginas.

### Ejemplo de uso:
```bash
python extractor.py --pdf "ruta/al/curso.pdf" --config secciones_solutions_architect.txt --output spanish/Knowledge_Base
```
