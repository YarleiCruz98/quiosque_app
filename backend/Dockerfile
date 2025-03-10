# Usar uma imagem oficial do Python
FROM python:3.10

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos para dentro do container
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar o Flask
CMD ["python", "run.py"]