# NapsterP2P

Implementação de um compartilhador de arquivos utilizando **sockets**, baseado no comportamento do **Napster**, conforme especificação da disciplina **Sistema Distribuído- 2025.1**.

## Descrição

O sistema segue um modelo **P2P** com servidor central para indexação:
- **Servidor**: mantém em memória a lista de usuários online e os arquivos que estão compartilhando.
- **Clientes**: enviam seus arquivos públicos ao servidor, pesquisam arquivos disponíveis e realizam downloads diretamente de outros clientes.

### Protocolo implementado
- **Cliente → Servidor**
  - `JOIN {IP-ADDRESS}`
  - `CREATEFILE {FILENAME} {SIZE}`
  - `DELETEFILE {FILENAME}`
  - `SEARCH {PATTERN}`
  - `LEAVE`
- **Servidor → Cliente**
  - `CONFIRMJOIN`
  - `CONFIRMCREATEFILE {FILENAME}`
  - `CONFIRMDELETEFILE {FILENAME}`
  - `CONFIRMLEAVE`
  - `FILE {FILENAME} {IP-ADDRESS} {SIZE}`
- **Cliente → Cliente**
  - `GET {FILENAME} {OFFSET START} [OFFSET END]`

---

## Estrutura de Pastas

```
NapsterP2P/
├── server.py        # Servidor central (porta 1234)
├── client.py        # Cliente P2P (porta 1235)
├── public/          # Pasta de arquivos compartilhados
└── downloads/       # Pasta onde os downloads são salvos
```

---

## Como executar

### 1. Preparar ambiente
Certifique-se de ter **Python 3** instalado.  
Crie as pastas `public` e `downloads` (se não existirem):

```bash
mkdir -p public downloads
```

Coloque alguns arquivos na pasta `public/` para compartilhar.

### 2. Rodar o servidor
Em um terminal:

```bash
python3 server.py
```

O servidor começará a escutar na porta **1234**.

### 3. Rodar um cliente
Em outro terminal:

```bash
python3 client.py
```

O cliente:
- envia `JOIN {IP}` ao servidor,
- compartilha todos os arquivos em `public/` via `CREATEFILE`,
- inicia um **menu interativo** para buscar, baixar arquivos e sair.

### 4. Rodar múltiplos clientes
Abra mais terminais e execute `client.py` novamente para simular outros usuários.

---

## Como usar o menu

1. **Buscar arquivo** – digite parte do nome (`SEARCH {PATTERN}`).
2. **Escolher arquivo para download** – o cliente mostra uma lista numerada dos arquivos encontrados.
3. **Baixar arquivo** – escolha pelo número; o arquivo será salvo em `downloads/`.
4. **Sair** – desconecta do servidor (`LEAVE`).

---

## Observações
- Cada cliente escuta na porta **1235** para enviar arquivos diretamente a outros clientes.
- Ao encerrar o cliente, o servidor remove o IP e arquivos associados da lista.
- O sistema segue estritamente o protocolo especificado.
