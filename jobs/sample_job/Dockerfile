# Obraz bazowy – oficjalny Spark z JDK17 i Pythonem
FROM spark:3.5.0-scala2.12-java17-python3-ubuntu

# Przechodzimy na roota, żeby zainstalować zależności
USER root

# Katalog aplikacji wewnątrz obrazu
WORKDIR /opt/app

# (Na razie opcjonalne) zależności Pythona – możesz zostawić pusty requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Kopiujemy kod joba – tu ma trafić main.py
COPY src/ ./src

# Ustawiamy PYTHONPATH, żeby Spark widział moduły z src
ENV PYTHONPATH=/opt/app/src:${PYTHONPATH}

# Wracamy do użytkownika spark (tak jest w obrazie bazowym)
USER spark

# ENTRYPOINT/CMD zostają z obrazu Spark – tego nie dotykamy
