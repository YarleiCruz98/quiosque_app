# quiosque_app

Descrição breve do projeto.

---

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter os seguintes pré-requisitos instalados:

- [Python](https://www.python.org/downloads/) 3.x
- [Docker](https://www.docker.com/products/docker-desktop)

---

## Configuração do Ambiente

### 1. Criar o Ambiente Virtual

Primeiro, crie um ambiente virtual para o projeto com o seguinte comando:

```bash
python -m venv venv

### 2. Criar o Ambiente Virtual

No Windows:
venv\Scripts\activate

No Linux/macOS:
source venv/bin/activate

### 3. Instalar Dependências
pip install -r requirements.txt

### 4. Subir os Contêineres com Docker
docker-compose up --build -d

## Rodando o Backend

###Dentro do Docker (Opcional)
docker exec -it backend python run.py

### 2. Fora do Docker (Opcional)
python run.py


### Para funcionar o frontend 

Para instalar devemos usar o comando:

# npm install ----> Assim instalamos o react
 
# npm run dev (dev é o comando imprestado do VITE)