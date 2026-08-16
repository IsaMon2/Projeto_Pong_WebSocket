# 🏓 Pong Multiplayer WebSocket

Projeto de um jogo **Pong Multiplayer** desenvolvido com **Python, HTML, CSS e JavaScript**, utilizando **WebSocket** para realizar a comunicação em tempo real entre dois jogadores.
O jogo permite que dois jogadores joguem em computadores diferentes conectados à mesma rede.

---

## 🎮 Sobre o projeto

O projeto é uma versão multiplayer do clássico jogo Pong.
Cada jogador controla uma raquete e deve impedir que a bola ultrapasse seu lado do campo.
A partida termina quando um dos jogadores alcança **5 pontos**. Após o final da partida, os jogadores podem clicar em **"Jogar Novamente"**. A nova partida só começa quando os dois jogadores estiverem prontos.

---

## 🎮 Controles

| Jogador   | Subir | Descer |
|    ---    |  ---  |   ---  | 
| Jogador 1 |  `W`  |  `S`   |
| Jogador 2 |  `↑`  |  `↓`   |

---

## 🛠️ Tecnologias utilizadas

- **Python** — servidor e lógica principal do jogo
- **WebSocket** — comunicação em tempo real
- **HTML5** — estrutura da interface
- **CSS3** — estilização
- **JavaScript** — interação com o jogo e comunicação com o servidor
- **Git/GitHub** — versionamento do projeto

---

## 📁 Estrutura do projeto

```text
Projeto_Pong_WebSocket/
│
├── server.py
├── test_client.py
├── requirements.txt
├── .gitignore
│
└── client/
    ├── index.html
    ├── style.css
    └── game.js
```
A pasta venv/ não é enviada para o GitHub. Cada usuário deve criar seu próprio ambiente virtual ao baixar o projeto.

---

## ⚙️ Requisitos

Para executar o projeto, é necessário ter:
- Python 3 instalado
- Git instalado
- Navegador atualizado
- Dois computadores conectados à mesma rede para testar o multiplayer

---

## 📥 Instalação

**1. Clonar o repositório**
Abra o terminal e execute:
```
git clone [https://github.com/IsaMon2/Projeto_Pong_WebSocket.git](https://github.com/IsaMon2/Projeto_Pong_WebSocket.git)
cd Projeto_Pong_WebSocket
```

**2. Criar o ambiente virtual**
Dentro da pasta do projeto, execute:
```
python -m venv venv
```
Esse comando cria um ambiente virtual chamado venv.
A pasta venv/ é local de cada computador e não deve ser enviada para o GitHub.

**3. Ativar o ambiente virtual**
Windows — PowerShell:
```
.\venv\Scripts\Activate.ps1
```
Quando estiver ativado, o terminal deverá apresentar algo parecido com:
```
(venv) PS C:\Users\...\Projeto_Pong_WebSocket>
```

Caso o PowerShell bloqueie a ativação:
Se aparecer uma mensagem informando que a execução de scripts foi bloqueada, execute:
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```
Essa alteração é válida somente para a sessão atual do PowerShell.

**4. Instalar as dependências**
Com a venv ativada, execute:
```
pip install -r requirements.txt
```
O arquivo requirements.txt contém as dependências necessárias para executar o servidor WebSocket.

--- 

## ▶️ Executando o projeto
O projeto utiliza dois servidores:
- WebSocket: porta 8080
- HTTP: porta 5500
Por isso, é necessário abrir dois terminais. A venv deve estar ativada em ambos os terminais.

**Terminal 1 — Servidor WebSocket**
Na pasta principal do projeto, execute:
```
python server.py
```
Se estiver funcionando corretamente, aparecerá algo parecido com:
```
Servidor WebSocket iniciado!
Rodando na porta 8080
Aguardando jogadores...
```
Mantenha esse terminal aberto durante toda a partida.

**Terminal 2 — Servidor HTTP**
Abra um segundo terminal, acesse a pasta do projeto e ative a venv:
```
cd Projeto_Pong_WebSocket
.\venv\Scripts\Activate.ps1
```
Depois execute:
```
python -m http.server 5500 --directory client
```
Mantenha esse terminal aberto durante toda a partida.

---

## 🌎 Acessando o jogo
No computador que está executando o servidor:
Abra o navegador e acesse:
``http://localhost:5500``

**Jogando em dois computadores**
Para jogar em dois computadores, os dois dispositivos precisam estar conectados à mesma rede Wi-Fi ou rede local.

1. Descobrir o endereço IP do servidor:
No computador que está executando o ``server.py``, abra um terminal e execute:
```
ipconfig
```
Procure pelo Endereço IPv4 (Exemplo: ``192.168.15.4``).

2. Acessar pelo segundo computador:
No segundo computador, abra o navegador e acesse:
``http://192.168.15.4:5500``
(Substitua ``192.168.15.4`` pelo endereço IPv4 do computador que está executando o servidor).

---

## 🏓 Funcionamento do Jogo e Multiplayer

Ao conectar, o primeiro jogador aguarda o segundo. Assim que o segundo jogador se conecta, a partida começa automaticamente.

**Arquitetura de Comunicação**
O arquivo ``server.py`` controla o estado principal da partida (bola, posições, colisões, placar e vitórias). A comunicação em tempo real acontece via WebSocket:
```
┌─────────────────┐             ┌────────────────────────┐             ┌─────────────────┐
│    Jogador 1    │  WebSocket  │       server.py        │  WebSocket  │    Jogador 2    │
│    game.js      ├────────────►│  • Bola                ├────────────►│    game.js      │
└─────────────────┘             │  • Raquetes            │             └─────────────────┘
                                │  • Colisões            │
                                │  • Placar / Vencedor   │
                                └────────────────────────┘
```

**Placar e Reinício**
- A partida é disputada até 5 pontos.
- Ao final da partida, é exibido o vencedor e o botão "Jogar Novamente".
- O jogo só recomeça quando ambos os jogadores clicarem no botão.

**Testando a conexão**
O projeto possui o arquivo ``test_client.py``, que pode ser utilizado para testes relacionados à comunicação isolada com o servidor WebSocket.

--- 

## 📌 Portas utilizadas

| Serviço       | Porta |
|      ---      |  ---  |   
| WebSocket     | 8080  |  
| Servidor HTTP | 5500  | 

---

## ⚠️ Possíveis problemas

- O segundo computador não consegue acessar o jogo:
  - Verifique se ambos estão na mesma rede.
  - Certifique-se de que os dois terminais (server.py e http.server) estão rodando.
  - Verifique se o Firewall do Windows não está bloqueando as portas 8080 e 5500.
- Erro de script no PowerShell ao ativar venv:
  - Execute Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass antes de reativar.

---

## 🛑 Encerrando o projeto

Para parar os servidores, vá em cada um dos terminais e pressione ``Ctrl + C``.

---

## 💌 Time

- Allana Aparecida Rizzo Ribeiro;
- Isabella Monsalles Barbosa;
- Joaquim Diglio;
- Maria Eduarda Torres

