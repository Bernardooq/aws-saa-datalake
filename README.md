# ☁️ AWS Certification Data Lake & Obsidian Knowledge Vault

Repositorio centralizado de estudio, apuntes arquitectónicos de alta fidelidad e índices interactivos optimizados para navegación en **Obsidian** y consumo por **LLMs / RAGs**.

---

## 📚 Certificaciones

| Certificación | Nivel | Directorio | Índice de Apuntes | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **AWS Solutions Architect Associate (SAA-C03)** | Associate | [`AWS_SAA-C03/`](./AWS_SAA-C03/) | [00_MOC_SAA-C03](./AWS_SAA-C03/spanish/00_MOC_SAA-C03.md) | ✅ 29 Módulos Completos |
| **AWS Cloud Practitioner (CLF-C02)** | Foundational | [`AWS_CLF-C02/`](./AWS_CLF-C02/) | *En preparación* | 🟡 Espacio Reservado |

---

## 🏛️ Estructura del Repositorio

```text
aws-saa-datalake/
├── README.md                                # Hub central del repositorio
├── .gitignore                               # Exclusiones de Git (PDFs, venvs, cache)
├── AWS_CLF-C02/                             # AWS Certified Cloud Practitioner
│   └── README.md
└── AWS_SAA-C03/                             # AWS Solutions Architect - Associate
    ├── README.md                            # Guía de la certificación y herramientas
    ├── extractor.py                         # CLI para extracción automatizada de cursos PDF
    ├── secciones_solutions_architect.txt   # Configuración de secciones del curso
    └── spanish/                             # Bóveda en Español (Obsidian Vault)
        ├── 00_MOC_SAA-C03.md                # Map of Content (Índice central de apuntes)
        └── Knowledge_Base/                  # 29 módulos organizados
            ├── 01_Primeros_pasos_con_AWS/
            │   ├── Primeros_pasos_con_AWS.md
            │   └── media/
            └── ...
```

---

## 🚀 Uso en Obsidian

1. Abre **Obsidian** y selecciona **"Open folder as vault"**.
2. **Recomendación:** Selecciona la carpeta raíz (`aws-saa-datalake`) para ver todas las certificaciones, o directamente [`AWS_SAA-C03/spanish`](./AWS_SAA-C03/spanish/) para enfocarte exclusivamente en Solutions Architect.
3. El archivo [`00_MOC_SAA-C03.md`](./AWS_SAA-C03/spanish/00_MOC_SAA-C03.md) es el punto de inicio para navegar por toda la base de conocimiento mediante enlaces bidireccionales y vista de grafo (`Ctrl + G`).
