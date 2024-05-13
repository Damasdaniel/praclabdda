# Usa una imagen base de Python con Flask preinstalado
FROM tiangolo/uwsgi-nginx-flask:python3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos de tu proyecto (si los tienes)
COPY requirements.txt requirements.txt

# Instala las dependencias de tu proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu aplicación al contenedor
COPY . .

# Expone el puerto en el que Flask escuchará las peticiones
EXPOSE 5000
