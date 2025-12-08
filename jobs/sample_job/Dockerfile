FROM bitnami/spark:3.5.0

USER root

# (opcjonalnie) dodatkowe pakiety systemowe
# RUN install_packages ...

# Zainstaluj zależności Pythona
COPY requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt

# Skopiuj kod joba
COPY src /opt/app/src

WORKDIR /opt/app

# Domyślna komenda — Spark driver uruchamia naszego maina
CMD ["spark-submit", "/opt/app/src/main.py"]
