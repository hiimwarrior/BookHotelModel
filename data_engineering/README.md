# Hotel Booking Demand Project

Este proyecto tiene como objetivo predecir la cancelación de reservas en un hotel utilizando datos históricos. Se implementa un pipeline de ciencia de datos usando DVC (Data Version Control) para versionar tanto los datos como el código.

## Estructura del Proyecto```plaintext
hotel_booking_project/
│
├── data/
│   ├── raw/                     # Datos crudos (sin procesar)
│   ├── processed/               # Datos procesados (limpios)
│   └── .gitignore               # Ignorar archivos de datos grandes
│
├── src/                         # Código fuente
│   ├── data/
│   │   ├── download_data.py     # Script para descargar los datos
│   │   └── clean_data.py        # Script para limpiar los datos
│   └── models/
│       └── train_model.py       # Script para entrenar el modelo de ML
│
├── dvc.yaml                     # Archivo de pipeline de DVC
├── dvc.lock                     # Archivo de bloqueos de DVC para versionado
├── .dvc/                        # Metadatos de DVC
├── .gitignore                   # Ignorar archivos de DVC y otros archivos grandes
├── README.md                    # Descripción del proyecto
└── requirements.txt             # Dependencias de Python