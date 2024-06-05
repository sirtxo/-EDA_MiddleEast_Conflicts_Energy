# Análisis de Conflictos y Acciones Energéticas en el Medio Oriente

Este proyecto realiza un análisis de conflictos y acciones energéticas en el Medio Oriente utilizando datos de la UCDP (Uppsala Conflict Data Program)
y datos históricos de precios de acciones de empresas energéticas.

## Archivos Utilizados y Generados

- **utils/**: Contiene scripts y funciones utilizados en el proyecto.
  - `get_data.py`: Script para obtener y procesar datos, generando los archivos CSV en `docs/`.
  - `functions.py`: Funciones utilitarias utilizadas en todo el proyecto.
  - `stocks_view.py`: Aplicación web para visualizar los datos CSV en un formato web.

- **notebooks/**: Contiene cuadernos Jupyter utilizados para el análisis.
  - **secondary/**: Contiene análisis iniciales por separado.
    - `Data_conflicts_analysis.ipynb`: Análisis de datos de conflictos.
    - `Data_index_analysis.ipynb`: Análisis de varios índices económicos.
    - `Ipc_Oil_Disasters_Initial_Analysis.ipynb`: Análisis inicial de datos del IPC, precios del petróleo y desastres.
  - `Conflicts_Analysis.ipynb`: Análisis completo de datos de conflictos incluyendo modelos de aprendizaje automático.
  - `StockAnalysis.ipynb`: Análisis de datos de acciones incluyendo predicciones de aprendizaje automático para `data.csv`.



## Otros Detalles

- Los archivos CSV generados se guardan en la carpeta 'docs' dentro del directorio padre.
- Se recomienda ejecutar los cuadernos Jupyter en un entorno de Jupyter Notebook o JupyterLab con las dependencias mencionadas instaladas.


## Librerías Utilizadas

- pandas: Para manipulación y análisis de datos.
- matplotlib: Para visualización de datos.
- numpy: Para cálculos numéricos.
- requests: Para realizar solicitudes HTTP y obtener datos de la UCDP API.
- yfinance: Para obtener datos históricos de precios de acciones.
- plotly: Para visualización interactiva de datos.


## Instrucciones de Uso

Para replicar el análisis realizado en este proyecto, sigue estos pasos:

1. Clona este repositorio en tu máquina local utilizando el siguiente comando:

git clone https://github.com/sirtxo/Finance_Eda.git


2. Asegúrate de tener instalado Python en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).

3. Instala las bibliotecas necesarias ejecutando el siguiente comando en tu terminal.

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar este proyecto, por favor, abre un issue o envía una pull request con tus sugerencias.

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).
