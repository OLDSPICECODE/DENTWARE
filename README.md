# DENT - Instalación y configuración

Este repositorio contiene el entorno de desarrollo para **Dentware**. Para configurar y comenzar a trabajar con este proyecto, sigue las instrucciones a continuación.

## Requisitos

- **Conda** instalado. Si no lo tienes, puedes descargarlo desde [aquí](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

## Instalación del entorno

1. **Clonar el repositorio** (si aún no lo has hecho):

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```
2. Crear el entorno con Conda usando el archivo environment.yml:

  ```bash
    conda env create -f environment.yml
   ```
3. Este comando creará un entorno Conda llamado DENT con todas las dependencias necesarias. Activar el entorno:

  ```bash
    conda activate DENT
   ```
