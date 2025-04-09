# Usar uma imagem do Node.js
FROM node:latest

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos essenciais primeiro (usando caminho correto)
COPY package.json package-lock.json ./

# Instalar dependências
RUN npm install

# Copiar todo o código da aplicação
COPY . . 

# Expor a porta do Vite
EXPOSE 5173

# Comando para rodar o Vite
CMD ["npm", "run", "dev"]
