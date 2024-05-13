# imagen base de Python con Flask preinstalado
FROM tiangolo/uwsgi-nginx-flask:python3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requisitos delproyecto 
COPY requirements.txt requirements.txt

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código al contenedor
COPY . .

# Puerto en el que Flask escuchará las peticiones
EXPOSE 5000
