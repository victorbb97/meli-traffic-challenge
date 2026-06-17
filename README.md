# meli-traffic-challenge

Projeto Python CLI para um desafio técnico com foco em **Support / Infrastructure**.

Python CLI project for a technical focused on Support / Infrastructure.


A aplicação lê pacotes a partir de um arquivo `.pcap` ou captura pacotes de uma interface de rede, armazena metadados normalizados em SQLite e exibe estatísticas básicas de tráfego no terminal.

O projeto foi mantido intencionalmente pequeno e objetivo para respeitar o escopo do desafio.

---

## O que este projeto faz

A CLI pode:

* ler pacotes a partir de um arquivo `.pcap` offline;
* capturar pacotes de uma interface de rede em tempo real;
* extrair metadados básicos dos pacotes;
* armazenar os dados extraídos em SQLite;
* exibir estatísticas básicas de tráfego no terminal;
* executar localmente ou dentro de Docker;
* executar testes automatizados sem depender de captura real de rede;
* validar diretamente no SQLite os metadados dos pacotes armazenados;
* gerar um `.pcap` sintético de demonstração com tráfego suficiente para preencher o Top 5 de IPs de origem e destino.

---

## Escopo

### Incluído

* Python CLI usando `argparse`
* Análise offline de pcap com `--pcap-file`
* Captura live de pacotes com `--interface`
* Armazenamento em SQLite usando a biblioteca padrão `sqlite3`
* Estatísticas básicas no terminal
* Dockerfile
* Testes automatizados objetivos
* Gerador offline de pcap para demonstração
* Passos de validação do armazenamento em SQLite
* Demonstração com mais de 30 IPs envolvidos e Top 5 preenchido

### Não incluído

* Frontend
* Web API
* Dashboard
* Authentication
* Queues
* External services
* External database
* ORM
* Async processing
* Complex logging system

---

## Requisitos

### Execução local

* Python 3.12+
* Scapy
* pytest

Instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Uso da CLI

Exibir ajuda:

```bash
python -m app.main --help
```

Argumentos esperados:

```txt
--interface
--timeout
--count
--db-path
--pcap-file
```

Argumentos disponíveis:

* `--interface`: nome da interface de rede para captura live, por exemplo `eth0`, `en0` ou `Wi-Fi`;
* `--timeout`: tempo máximo da captura live em segundos;
* `--count`: quantidade máxima de pacotes a processar;
* `--db-path`: caminho do banco SQLite;
* `--pcap-file`: caminho opcional para arquivo pcap usado na análise offline.

Se nem `--pcap-file` nem `--interface` forem informados, a CLI retorna uma mensagem amigável orientando o uso correto.

---

## Análise offline de pcap

Use este modo quando você já possui um arquivo `.pcap`:

```bash
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

Este é o modo mais previsível para testes e demonstrações, porque não depende de permissões de rede, drivers do sistema operacional ou capacidades de rede do Docker.

---

## Demonstração offline com pcap gerado

O repositório inclui um script auxiliar para gerar um arquivo `.pcap` reproduzível com pacotes TCP, UDP e ICMP.

O arquivo gerado simula um tráfego maior, com mais de 30 endereços IP envolvidos no total. A distribuição dos pacotes foi criada para preencher claramente:

* Top 5 endereços IP de origem;
* Top 5 endereços IP de destino;
* contagem por protocolo;
* total de pacotes capturados.

Gerar o pcap de teste:

```bash
python scripts/generate_test_pcap.py
```

Arquivo gerado:

```txt
samples/test.pcap
```

Executar o analyzer:

```bash
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

Para uma demonstração limpa, remova o banco local anterior antes da execução.

No Linux/macOS:

```bash
rm -f traffic.db
python scripts/generate_test_pcap.py
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

No Windows PowerShell:

```powershell
Remove-Item traffic.db -Force -ErrorAction SilentlyContinue
python scripts/generate_test_pcap.py
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

Formato esperado da saída após uma execução limpa:

```txt
=== Traffic Analysis Summary ===

Total packets captured: 56

Packets by protocol:
ICMP: X
TCP: X
UDP: X

Top 5 source IPs:
1. 10.0.0.1 - 12 packets
2. 10.0.0.2 - 10 packets
3. 10.0.0.3 - 8 packets
4. 10.0.0.4 - 6 packets
5. 10.0.0.5 - 5 packets

Top 5 destination IPs:
1. 203.0.113.10 - 13 packets
2. 203.0.113.20 - 11 packets
3. 203.0.113.30 - 9 packets
4. 203.0.113.40 - 7 packets
5. 203.0.113.50 - 6 packets
```

Se o mesmo banco for reutilizado em múltiplas execuções, os totais podem aumentar porque a aplicação armazena cada pacote processado no SQLite.

Para testes repetíveis, exclua o arquivo `traffic.db` antes de cada execução.

---

## Validar pacotes armazenados no SQLite

Após executar a análise offline, inspecione o banco SQLite para confirmar que os metadados dos pacotes foram realmente armazenados.

Este passo valida o requisito de armazenamento em banco de dados, não apenas a saída exibida no terminal.

No Windows PowerShell:

```powershell
@'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])

    print()
    print("Top 5 source IPs from DB:")
    for row in cursor.execute("""
        SELECT source_ip, COUNT(*)
        FROM packets
        GROUP BY source_ip
        ORDER BY COUNT(*) DESC, source_ip ASC
        LIMIT 5;
    """):
        print(row)

    print()
    print("Top 5 destination IPs from DB:")
    for row in cursor.execute("""
        SELECT destination_ip, COUNT(*)
        FROM packets
        GROUP BY destination_ip
        ORDER BY COUNT(*) DESC, destination_ip ASC
        LIMIT 5;
    """):
        print(row)
'@ | python -
```

No Linux/macOS:

```bash
python - <<'PY'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])

    print()
    print("Top 5 source IPs from DB:")
    for row in cursor.execute("""
        SELECT source_ip, COUNT(*)
        FROM packets
        GROUP BY source_ip
        ORDER BY COUNT(*) DESC, source_ip ASC
        LIMIT 5;
    """):
        print(row)

    print()
    print("Top 5 destination IPs from DB:")
    for row in cursor.execute("""
        SELECT destination_ip, COUNT(*)
        FROM packets
        GROUP BY destination_ip
        ORDER BY COUNT(*) DESC, destination_ip ASC
        LIMIT 5;
    """):
        print(row)
PY
```

Isso confirma que a aplicação persistiu os campos exigidos:

* `captured_at`
* `source_ip`
* `destination_ip`
* `protocol`
* `packet_size`

---

## Captura live

Exemplo:

```bash
python -m app.main --interface eth0 --timeout 60 --count 100 --db-path traffic.db
```

A captura live pode exigir privilégios de administrador/root, Npcap no Windows ou capacidades Linux como `NET_RAW` e `NET_ADMIN`.

O modo offline com pcap é recomendado para testes previsíveis e demonstrações em entrevista.

---

## Saída

O resumo no terminal segue este formato:

```txt
=== Traffic Analysis Summary ===

Total packets captured: X

Packets by protocol:
TCP: X
UDP: X
ICMP: X
NON_IP: X

Top 5 source IPs:
1. 10.0.0.1 - X packets
2. 10.0.0.2 - X packets
3. 10.0.0.3 - X packets
4. 10.0.0.4 - X packets
5. 10.0.0.5 - X packets

Top 5 destination IPs:
1. 203.0.113.10 - X packets
2. 203.0.113.20 - X packets
3. 203.0.113.30 - X packets
4. 203.0.113.40 - X packets
5. 203.0.113.50 - X packets
```

As estatísticas são calculadas a partir dos pacotes armazenados no banco SQLite.

---

## Schema SQLite

A aplicação cria uma tabela chamada `packets`:

```sql
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at TEXT NOT NULL,
    source_ip TEXT,
    destination_ip TEXT,
    protocol TEXT NOT NULL,
    packet_size INTEGER NOT NULL
);
```

Campos armazenados:

| Field            | Description                                                      |
| ---------------- | ---------------------------------------------------------------- |
| `captured_at`    | UTC timestamp gerado durante o processamento                     |
| `source_ip`      | Endereço IPv4 ou IPv6 de origem, ou `NULL` para pacotes non-IP   |
| `destination_ip` | Endereço IPv4 ou IPv6 de destino, ou `NULL` para pacotes non-IP  |
| `protocol`       | Protocolo do pacote, como `TCP`, `UDP`, `ICMP`, `IP` ou `NON_IP` |
| `packet_size`    | Tamanho do pacote calculado com `len(packet)`                    |

O payload bruto dos pacotes não é armazenado.

---

## Docker

Build da imagem:

```bash
docker build -t meli-traffic-challenge .
```

Executar help dentro do Docker:

```bash
docker run --rm meli-traffic-challenge --help
```

Executar com arquivo pcap montado a partir do diretório atual no Linux/macOS:

```bash
docker run --rm -v "$PWD:/data" meli-traffic-challenge --pcap-file /data/samples/test.pcap --db-path /data/traffic.db
```

Executar com arquivo pcap montado a partir do diretório atual no Windows PowerShell:

```powershell
$projectPath = (Get-Location).Path

docker run --rm `
  -v "${projectPath}:/data" `
  meli-traffic-challenge `
  --pcap-file /data/samples/test.pcap `
  --db-path /data/traffic.db
```

Observação: não é necessário usar `--name` no container. Rodar sem nome evita conflito caso exista um container antigo parado com o mesmo nome.

Executar captura live no Docker em Linux:

```bash
docker run --rm --net=host --cap-add=NET_RAW --cap-add=NET_ADMIN meli-traffic-challenge --interface eth0 --timeout 60 --count 100 --db-path /tmp/traffic.db
```

A captura live dentro do Docker depende do sistema operacional host, do modo de rede do Docker e das capabilities concedidas.

---

## Testes

Executar validação de sintaxe:

```bash
python -m compileall app tests scripts
```

Executar testes automatizados no Linux/macOS:

```bash
python -m pytest tests -p no:cacheprovider
```

Executar testes automatizados no Windows PowerShell usando uma pasta temporária única por execução:

```powershell
$runId = [guid]::NewGuid().ToString("N")
$baseTemp = "tmp/pytest-$runId"

New-Item -ItemType Directory -Force -Path tmp | Out-Null

python -m pytest tests -p no:cacheprovider --basetemp="$baseTemp"
```

Resultado esperado com sucesso:

```txt
collected 7 items

tests/test_cli.py ...
tests/test_statistics.py ..
tests/test_storage.py ..

7 passed
```

Os testes cobrem:

* comportamento do parser da CLI;
* criação do schema SQLite;
* inserção básica de pacotes;
* cálculo de estatísticas de tráfego.

Os testes não dependem de captura real de rede.

---

## Checklist completo de validação local

Use esta checklist antes de submeter ou enviar alterações.

### 1. Verificar help

```bash
python -m app.main --help
```

Resultado esperado:

* o comando finaliza com sucesso;
* todos os argumentos esperados são exibidos.

### 2. Compilar arquivos-fonte

```bash
python -m compileall app tests scripts
```

Resultado esperado:

* nenhum erro de sintaxe.

### 3. Executar testes automatizados

No Linux/macOS:

```bash
python -m pytest tests -p no:cacheprovider
```

No Windows PowerShell:

```powershell
$runId = [guid]::NewGuid().ToString("N")
$baseTemp = "tmp/pytest-$runId"

New-Item -ItemType Directory -Force -Path tmp | Out-Null

python -m pytest tests -p no:cacheprovider --basetemp="$baseTemp"
```

Resultado esperado:

* todos os testes passam;
* saída esperada: `7 passed`.

### 4. Gerar pcap de teste

```bash
python scripts/generate_test_pcap.py
```

Resultado esperado:

```txt
Generated pcap: samples/test.pcap
```

No Windows, o Scapy pode exibir o seguinte warning:

```txt
WARNING: No libpcap provider available ! pcap won't be used
```

Para a geração e leitura offline do `.pcap`, esse aviso não impede a demonstração.

### 5. Executar análise offline com banco limpo

No Linux/macOS:

```bash
rm -f traffic.db
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

No Windows PowerShell:

```powershell
Remove-Item traffic.db -Force -ErrorAction SilentlyContinue
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db
```

Resultado esperado:

* o resumo é exibido no terminal;
* o total de pacotes é exibido;
* os protocolos são agrupados;
* os 5 principais IPs de origem são exibidos;
* os 5 principais IPs de destino são exibidos;
* o arquivo `traffic.db` é criado localmente.

### 6. Validar armazenamento SQLite

No Windows PowerShell:

```powershell
@'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])
'@ | python -
```

No Linux/macOS:

```bash
python - <<'PY'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])
PY
```

Resultado esperado:

* os pacotes armazenados são listados;
* os campos exigidos ficam visíveis;
* o total corresponde à execução limpa da demonstração.

### 7. Build da imagem Docker

```bash
docker build -t meli-traffic-challenge .
```

Resultado esperado:

* a imagem Docker é construída com sucesso.

### 8. Executar help no Docker

```bash
docker run --rm meli-traffic-challenge --help
```

Resultado esperado:

* o help da CLI é exibido dentro do container.

### 9. Executar análise offline no Docker

No Linux/macOS:

```bash
docker run --rm -v "$PWD:/data" meli-traffic-challenge --pcap-file /data/samples/test.pcap --db-path /data/traffic.db
```

No Windows PowerShell:

```powershell
$projectPath = (Get-Location).Path

docker run --rm `
  -v "${projectPath}:/data" `
  meli-traffic-challenge `
  --pcap-file /data/samples/test.pcap `
  --db-path /data/traffic.db
```

Resultado esperado:

* o resumo do tráfego é exibido dentro do container;
* o banco `traffic.db` é criado/atualizado no diretório do projeto por meio do volume montado.

---

## Arquivos locais de runtime

Os arquivos abaixo são artefatos locais de execução e não devem ser commitados:

```txt
traffic.db
*.db
*.sqlite
*.sqlite3
samples/test.pcap
*.pcap
*.pcapng
tmp/
pytest_temp/
.pytest-tmp/
.pytest_cache/
__pycache__/
```

---

## Troubleshooting

### `WARNING: No libpcap provider available ! pcap won't be used`

Este warning pode aparecer no Windows quando o Scapy não encontra um provider libpcap/Npcap.

Para leitura offline de pcap, a aplicação pode continuar funcionando normalmente.

Para captura live no Windows, instale o Npcap e execute o terminal com as permissões necessárias.

### O total de pacotes está maior que o esperado

O banco SQLite armazena os pacotes processados.

Se o mesmo `traffic.db` for reutilizado, os totais podem acumular entre execuções.

Exclua o banco antes de uma demonstração limpa:

```powershell
Remove-Item traffic.db -Force -ErrorAction SilentlyContinue
```

ou:

```bash
rm -f traffic.db
```

### Docker retorna erro ao clicar em Play no Docker Desktop

A aplicação é uma CLI e precisa receber argumentos.

Se o container for iniciado pela interface do Docker Desktop sem argumentos, a aplicação pode retornar:

```txt
Error: provide --pcap-file for offline analysis or --interface for live capture.
```

Isso é esperado.

Execute pelo terminal informando `--pcap-file` ou `--interface`.

### Docker retorna conflito de nome de container

Se for usado `--name meli-container` e já existir um container com esse nome, o Docker pode retornar conflito.

Solução simples:

```bash
docker rm meli-container
```

Ou rode sem `--name`, que é o recomendado para esta demonstração.

### Docker live capture não recebe pacotes

A captura live dentro do Docker depende do sistema operacional host, do modo de rede do Docker e das capabilities concedidas.

No Linux, tente:

```bash
docker run --rm --net=host --cap-add=NET_RAW --cap-add=NET_ADMIN meli-traffic-challenge --interface eth0 --timeout 60 --count 100
```

No Windows/macOS com Docker Desktop, o modo offline com pcap é mais confiável para validação.

### Pytest no Windows retorna `PermissionError`

Em alguns ambientes Windows, o Pytest pode travar ao reutilizar/remover pastas temporárias.

Use um `basetemp` único por execução:

```powershell
$runId = [guid]::NewGuid().ToString("N")
$baseTemp = "tmp/pytest-$runId"

New-Item -ItemType Directory -Force -Path tmp | Out-Null

python -m pytest tests -p no:cacheprovider --basetemp="$baseTemp"
```

---

## Decisões técnicas

### Python

Python foi escolhido por ser prático para automação de infraestrutura, análise de pacotes e ferramentas CLI.

### Scapy

Scapy foi escolhido porque oferece suporte tanto à leitura offline de pcap quanto à captura live de pacotes com pouco código.

### SQLite

SQLite foi utilizado por meio do módulo padrão `sqlite3` do Python para evitar configuração de banco externo.

O desafio exige armazenamento em banco de dados, mas não exige um servidor de banco.

### No ORM

Nenhum ORM foi utilizado porque o schema é pequeno e SQL explícito é mais simples de revisar neste contexto.

### Arquitetura pequena

A arquitetura permanece intencionalmente pequena:

```txt
CLI -> Capture -> SQLite -> Statistics
```

Isso mantém a solução simples de executar, testar e explicar em entrevista.

### PCAP sintético para demonstração

O script `scripts/generate_test_pcap.py` existe apenas para gerar uma massa de tráfego offline e reproduzível.

Ele não altera a arquitetura principal da aplicação.

---

## Estrutura do projeto

A estrutura versionada do repositório é intencionalmente pequena:

```txt
meli-traffic-challenge/
 app/
    __init__.py
    capture.py
    cli.py
    main.py
    statistics.py
    storage.py
 docs/
    architecture.md
    context-sprint.md
 scripts/
    generate_test_pcap.py
 tests/
    __init__.py
    test_cli.py
    test_statistics.py
    test_storage.py
 .dockerignore
 .gitattributes
 .gitignore
 Dockerfile
 pytest.ini
 README.md
 requirements.txt
```

Durante a execução local e os testes, os seguintes arquivos e pastas gerados podem aparecer no workspace:

```txt
meli-traffic-challenge/
 .pytest_cache/
 app/
    __pycache__/
 samples/
    test.pcap
 scripts/
    __pycache__/
 tests/
    __pycache__/
 tmp/
    pytest-*/
 traffic.db
```

Esses artefatos gerados são esperados durante a validação local e não devem ser commitados.

---

## Sequência final de validação

No Windows PowerShell:

```powershell
python -m app.main --help
python -m compileall app tests scripts

$runId = [guid]::NewGuid().ToString("N")
$baseTemp = "tmp/pytest-$runId"

New-Item -ItemType Directory -Force -Path tmp | Out-Null

python -m pytest tests -p no:cacheprovider --basetemp="$baseTemp"

Remove-Item traffic.db -Force -ErrorAction SilentlyContinue
python scripts/generate_test_pcap.py
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db

@'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])
'@ | python -

docker build -t meli-traffic-challenge .
docker run --rm meli-traffic-challenge --help

$projectPath = (Get-Location).Path

docker run --rm `
  -v "${projectPath}:/data" `
  meli-traffic-challenge `
  --pcap-file /data/samples/test.pcap `
  --db-path /data/traffic.db
```

No Linux/macOS:

```bash
python -m app.main --help
python -m compileall app tests scripts
python -m pytest tests -p no:cacheprovider

rm -f traffic.db
python scripts/generate_test_pcap.py
python -m app.main --pcap-file samples/test.pcap --db-path traffic.db

python - <<'PY'
import sqlite3

with sqlite3.connect("traffic.db") as connection:
    cursor = connection.cursor()

    print("Stored packets:")
    for row in cursor.execute("""
        SELECT id, captured_at, source_ip, destination_ip, protocol, packet_size
        FROM packets
        ORDER BY id ASC
        LIMIT 10;
    """):
        print(row)

    print()
    print("Total:")
    print(cursor.execute("SELECT COUNT(*) FROM packets;").fetchone()[0])
PY

docker build -t meli-traffic-challenge .
docker run --rm meli-traffic-challenge --help
docker run --rm -v "$PWD:/data" meli-traffic-challenge --pcap-file /data/samples/test.pcap --db-path /data/traffic.db
```

---

## Status de validação atual

Validações realizadas durante a Sprint 01:

```txt
python -m app.main --help                           OK
python -m compileall app tests scripts              OK
python -m pytest com basetemp único no Windows      OK, 7 passed
docker build -t meli-traffic-challenge .            OK
python scripts/generate_test_pcap.py                OK
python -m app.main --pcap-file samples/test.pcap    OK
SQLite traffic.db criado e consultável              OK
```

Resultado da demonstração offline com PCAP sintético:

```txt
Total packets captured: 56

Top 5 source IPs:
1. 10.0.0.1 - 12 packets
2. 10.0.0.2 - 10 packets
3. 10.0.0.3 - 8 packets
4. 10.0.0.4 - 6 packets
5. 10.0.0.5 - 5 packets

Top 5 destination IPs:
1. 203.0.113.10 - 13 packets
2. 203.0.113.20 - 11 packets
3. 203.0.113.30 - 9 packets
4. 203.0.113.40 - 7 packets
5. 203.0.113.50 - 6 packets
```
