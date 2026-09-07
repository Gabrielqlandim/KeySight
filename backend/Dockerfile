# Imagem base: Python 3.12 na variante "slim" (Debian enxuto, sem
# ferramentas gráficas nem compiladores extras) — menor e mais rápida
# de baixar que a imagem "completa". Usamos 3.12 em vez do 3.13 mais
# recente porque o psycopg2-binary (driver do Postgres) ainda não
# publica um wheel pronto para 3.13 nesta versão, o que forçaria a
# compilação a partir do código-fonte dentro do container.
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container. Todos os comandos
# seguintes (COPY, RUN, CMD) rodam a partir daqui.
WORKDIR /app

# Copiamos só o requirements.txt primeiro (antes do resto do código).
# Isso é uma otimização de cache do Docker: se o código mudar mas as
# dependências não, o Docker reaproveita a camada já instalada em vez
# de rodar `pip install` de novo a cada build.
COPY requirements.txt .

# --no-cache-dir evita que o pip guarde um cache de pacotes dentro da
# imagem, deixando-a menor.
RUN pip install --no-cache-dir -r requirements.txt

# Agora sim copiamos o restante do código da aplicação.
COPY . .

# Comando executado quando o container sobe: inicia o uvicorn servindo
# o objeto `app` de `app/main.py`.
# --host 0.0.0.0 é obrigatório em containers: "0.0.0.0" significa
# "escute em todas as interfaces de rede", não só localhost interno do
# container — sem isso, o Docker Compose não conseguiria expor a porta
# para fora.
# --reload reinicia o servidor automaticamente quando o código muda
# (ótimo para desenvolvimento; será removido na imagem de produção).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
