# Imagem de desenvolvimento do frontend. Node 22 na variante "slim"
# (o mesmo Node que você já tem instalado localmente).
FROM node:22-slim

WORKDIR /app

# Mesma otimização de cache que fizemos no backend: copia só os
# arquivos que descrevem as dependências antes do resto do código.
COPY package.json package-lock.json ./
RUN npm install

COPY . .

# Porta padrão do servidor de desenvolvimento do Vite.
EXPOSE 5173

# "-- --host 0.0.0.0" repassa a flag pro Vite (o "--" separa os
# argumentos do npm dos argumentos do script). Já configuramos isso
# também em vite.config.js; a flag aqui é redundante mas explícita.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
