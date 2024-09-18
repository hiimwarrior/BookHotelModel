# Proyecto MLOps - Bootcamp

Este documento proporciona una descripción general del proyecto final del bootcamp de MLOps. El proyecto está diseñado para demostrar el uso de infraestructura como código, herramientas de control de versiones de datos, y buenas prácticas de desarrollo de modelos de machine learning.

## Estructura de Carpetas

A continuación se detalla la estructura de carpetas del proyecto:

.dvc/ # Directorio para la configuración y metadatos de DVC (Data Version Control)

.pytest_cache/ # Caché de pruebas de pytest

.ruff_cache/ # Caché de ruff

api/ # Código fuente y configuración para el API del proyecto

data/ # Datos crudos utilizados en el proyecto

data_engineering/ # Scripts y configuraciones para el procesamiento de datos src/ # Código fuente para la ingeniería de datos transformation/ # Transformaciones de datos específicas

data_science/ # Scripts y modelos de ciencia de datos

infra/ # Infraestructura como código (IaC) y configuraciones de infraestructura docker-compose.yml Dockerfile

scripts/ # Scripts de utilidad y automatización cli.sh # Otros scripts

streamlit_apps/ # Aplicaciones desarrolladas con Streamlit para la visualización de datos

.dvcignore .gitignore .ruff.toml cli.sh CLI_DOCS.md dvc.lock dvc.yaml README.md

## Apartado de Desarrollador

### CLI para Comandos Locales

El proyecto incluye un script CLI que facilita la gestión de tareas relacionadas con DVC, configuraciones de base de datos, inicialización de datos, linting, pruebas y la interfaz de usuario de MLflow. A continuación se presenta un resumen de los comandos principales disponibles en el script `cli.sh`:

- **`dvc-init-pipeline`**: Inicializa DVC, configura el entorno virtual y ejecuta el pipeline de DVC.
- **`setup-db [ENV]`**: Configura y arranca los contenedores de base de datos para el entorno especificado (`prod`, `local`, `test`).
- **`initialize-data [VERSION] [DESTINATION]`**: Procesa y llena datos según la versión de transformación y destino (`csv` o `db`).
- **`lint [DIRECTORY]`**: Ejecuta las comprobaciones de linting en el directorio especificado (`api`, `data_science`, `data_engineering`, o `all`).
- **`test [DIRECTORY]`**: Ejecuta las pruebas en el directorio especificado (`api`, `data_engineering`, `data_science`).
- **`start-mlflow-ui`**: Inicia el servidor de la interfaz de usuario de MLflow.

Para obtener información detallada sobre los comandos y sus opciones, consulta el archivo [CLI_DOCS.md](CLI_DOCS.md).

## Arquitectura

### Diagrama de Arquitectura

A continuación se muestra el diagrama de arquitectura del sistema:

![Diagrama de Arquitectura](path_to_architecture_diagram.png)

#### Fase 1: Infraestructura como Código

En la primera fase del proyecto, se emplea infraestructura como código (IaC) para montar los componentes principales del sistema. La configuración de la infraestructura se encuentra en el directorio `infra`, donde se utiliza `Terraform` para definir y gestionar la infraestructura en la nube. `Terraform` permite configurar recursos en AWS, como instancias EC2, redes y almacenamiento, facilitando la gestión y despliegue de los componentes de infraestructura necesarios.

Además, se utilizan `docker-compose` y `Dockerfile` para definir y construir los servicios necesarios, asegurando que todos los componentes se ejecuten de manera consistente en contenedores Docker.

Las acciones más importantes se orquestan mediante un servicio de **Apache Airflow** ejecutado en el servidor. Airflow gestiona y programa los flujos de trabajo, asegurando la correcta ejecución de las tareas de procesamiento y modelado, integrándose con los recursos configurados a través de Terraform.


## Modelo

### Descripción del Modelo

El proyecto incluye un modelo de machine learning diseñado para predecir cancelaciones de reservas de hotel. Las principales características del modelo son:

- **Tipo de Modelo:** [Especificar el tipo, e.g., Regresión Logística, Random Forest, etc.]
- **Algoritmos Utilizados:** [Especificar los algoritmos, e.g., XGBoost, LSTM, etc.]
- **Métricas de Evaluación:** [Especificar las métricas, e.g., Accuracy, Precision, Recall, F1 Score, etc.]

#### Gráficas

A continuación se presentan algunas gráficas que ilustran el desempeño del modelo:

- **Matriz de Confusión:**
  ![Matriz de Confusión](path_to_confusion_matrix.png)

- **Curva ROC:**
  ![Curva ROC](path_to_roc_curve.png)

- **Importancia de Características:**
  ![Importancia de Características](path_to_feature_importance.png)

Para más detalles sobre el modelo y su rendimiento, consulta la carpeta `data_science` donde se encuentran los notebooks y scripts relevantes.

