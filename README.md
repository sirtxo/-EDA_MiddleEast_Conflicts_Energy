# Análisis de Conflictos y Acciones Energéticas en el Medio Oriente

Este proyecto realiza un análisis de conflictos y acciones energéticas en el Medio Oriente utilizando datos de la UCDP (Uppsala Conflict Data Program)
y datos históricos de precios de acciones de empresas energéticas.

## Archivos Utilizados y Generados

1. **Data_Initial_Analisis.ipynb**:
   - Cuaderno Jupyter utilizado para explorar inicialmente los datos de la UCDP y establecer países del Medio Oriente como foco de análisis.

2. **Data_Analisis.ipynb**:
   - Cuaderno Jupyter que realiza un análisis más profundo de los datos de la UCDP, centrándose en países del Medio Oriente, y correlaciona eventos de conflicto con cambios en precios de acciones.

3. **get_data.py**:
   - Script Python utilizado para obtener los datos necesarios para el Análisis Exploratorio de Datos (EDA).
   - Este script descarga y guarda en archivos CSV los datos de eventos de la UCDP y datos históricos de precios de acciones de empresas energéticas.

## Librerías Utilizadas

- pandas: Para manipulación y análisis de datos.
- matplotlib: Para visualización de datos.
- numpy: Para cálculos numéricos.
- requests: Para realizar solicitudes HTTP y obtener datos de la UCDP API.
- yfinance: Para obtener datos históricos de precios de acciones.
- plotly: Para visualización interactiva de datos.

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
