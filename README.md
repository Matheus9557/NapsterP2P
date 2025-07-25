# NapsterP2P

Projeto acadêmico: Implementação de um **compartilhador de arquivos P2P** baseado no funcionamento do **Napster** utilizando **sockets** em Python.  
Desenvolvido para a disciplina **Sistema Distribuído - 2025.1**.

---

## 📖 Descrição do Sistema

O projeto segue uma arquitetura **P2P assistida por servidor central**:
- **Servidor (porta 1234)**: mantém em memória todos os clientes conectados e os arquivos que compartilham.
- **Clientes (porta 1235)**:
  - Enviam suas informações e arquivos públicos ao servidor (`JOIN` e `CREATEFILE`).
  - Realizam buscas (`SEARCH`) e recebem a lista de arquivos disponíveis.
  - Baixam arquivos diretamente de outros clientes (`GET`).

O sistema segue **estritamente o protocolo especificado** na atividade, garantindo compatibilidade e simplicidade.

---

## 📂 Estrutura do Projeto

```
NapsterP2P/
├── server.py        # Servidor central - gerenciamento de clientes e arquivos
├── client.py        # Cliente P2P - envia arquivos, busca e realiza downloads
├── public/          # Pasta com arquivos que serão compartilhados
└── downloads/       # Pasta onde arquivos baixados serão salvos
```

- **public/**: coloque aqui os arquivos que deseja compartilhar.
- **downloads/**: será criada automaticamente ao baixar arquivos.

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.x instalado
- Sistema operacional compatível (Linux, Windows ou macOS)

### Passos:

1. **Criar as pastas necessárias**
   ```bash
   mkdir -p public downloads
   ```

2. **Executar o servidor**
   ```bash
   python3 server.py
   ```
   O servidor ficará escutando na porta **1234**.

3. **Executar um cliente**
   ```bash
   python3 client.py
   ```
   - Envia automaticamente:
     - `JOIN {IP-ADDRESS}`
     - `CREATEFILE {FILENAME} {SIZE}` para todos arquivos em `public/`.
   - Abre um menu interativo para buscas e downloads.

4. **Adicionar mais clientes**
   - Execute `python3 client.py` em outras janelas de terminal para simular usuários adicionais.

---

## 🧭 Menu Interativo do Cliente

1. **Buscar arquivo**
   - Digite parte do nome.  
   - Exemplo: `.mp3` → retorna todos arquivos com `.mp3` no nome.

2. **Baixar arquivo**
   - O sistema exibe uma lista numerada dos resultados da busca.
   - Escolha o número do arquivo para baixar.  
   - O arquivo será salvo em `downloads/`.

3. **Sair**
   - Envia `LEAVE` ao servidor, removendo o cliente da lista.

---

## 📡 Protocolo Implementado

### Cliente → Servidor
- `JOIN {IP-ADDRESS}`
- `CREATEFILE {FILENAME} {SIZE}`
- `DELETEFILE {FILENAME}`
- `SEARCH {PATTERN}`
- `LEAVE`

### Servidor → Cliente
- `CONFIRMJOIN`
- `CONFIRMCREATEFILE {FILENAME}`
- `CONFIRMDELETEFILE {FILENAME}`
- `CONFIRMLEAVE`
- `FILE {FILENAME} {IP-ADDRESS} {SIZE}`

### Cliente → Cliente
- `GET {FILENAME} {OFFSET START} [OFFSET END]`

---

## 📝 Observações Importantes
- Certifique-se de que cada cliente esteja rodando em uma porta 1235 livre.
- Para encerrar o servidor, use `Ctrl + C` no terminal onde ele está rodando.
- Arquivos baixados mantêm o nome original do arquivo compartilhado.
- Em caso de conflito de portas, finalize processos que estejam ocupando-as:
  ```bash
  sudo fuser -k 1234/tcp
  sudo fuser -k 1235/tcp
  ```

---

## 📌 Próximos Passos
1. **Versionar o projeto**
   ```bash
   git init
   git add .
   git commit -m "Implementação inicial NapsterP2P"
   ```

2. **Criar repositório no GitHub** e conectar:
   ```bash
   git branch -M main
   git remote add origin https://github.com/seu-usuario/NapsterP2P.git
   git push -u origin main
   ```

---
