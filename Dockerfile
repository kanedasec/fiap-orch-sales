# Usando Python 3.12 slim
FROM python:3.12-slim

# Configura diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (caso precise do psycopg2, etc)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copia os requirements
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta do serviço
EXPOSE 8004

# Comando para rodar o serviço
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8005"]
