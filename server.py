import asyncio
import websockets
import json

jogadores = {}

# =========================
# POSIÇÃO DA BOLA
# =========================

ball_x = 390
ball_y = 240

# =========================
# VELOCIDADE DA BOLA
# =========================

ball_speed_x = 4
ball_speed_y = 4

# =========================
# POSIÇÃO DAS RAQUETES
# =========================

player1_y = 200
player2_y = 200

# =========================
# PLACAR
# =========================

player1_score = 0
player2_score = 0

# =========================
# CONTROLE DA PARTIDA
# =========================

game_over = False

# Jogadores que clicaram em "Jogar Novamente"
jogadores_prontos = set()


# ==================================================
# CONEXÃO DOS JOGADORES
# ==================================================

async def conectar(websocket):

    global player1_y, player2_y
    global player1_score, player2_score
    global ball_x, ball_y
    global ball_speed_x, ball_speed_y
    global game_over
    global jogadores_prontos

    # Só permite dois jogadores
    if len(jogadores) >= 2:

        await websocket.send("Jogo cheio!")
        await websocket.close()

        return

    # Define o número do jogador
    if 1 not in jogadores:
        jogador = 1
    else:
        jogador = 2

    jogadores[jogador] = websocket

    print(f"Jogador {jogador} conectado!")

    # ==================================================
    # QUANDO OS DOIS JOGADORES ESTIVEREM CONECTADOS
    # ==================================================

    if len(jogadores) == 2:

        player1_score = 0
        player2_score = 0

        player1_y = 200
        player2_y = 200

        ball_x = 390
        ball_y = 240

        ball_speed_x = 4
        ball_speed_y = 4

        game_over = False

        jogadores_prontos.clear()

        print("Nova partida iniciada!")

        # Avisa os dois jogadores
        for jogador_atual in list(jogadores.values()):

            try:

                await jogador_atual.send(
                    "NOVA_PARTIDA"
                )

            except websockets.exceptions.ConnectionClosed:

                pass

    # ==================================================
    # INFORMA QUAL JOGADOR É
    # ==================================================

    await websocket.send(
        f"Você é o jogador {jogador}"
    )

    # ==================================================
    # ENVIA O PLACAR ATUAL
    # ==================================================

    await websocket.send(
        f"PLACAR:{player1_score},{player2_score}"
    )

    # ==================================================
    # SE SÓ TIVER UM JOGADOR
    # ==================================================

    if len(jogadores) == 1:

        await websocket.send(
            "AGUARDANDO"
        )

    # ==================================================
    # RECEBE MENSAGENS
    # ==================================================

    try:

        async for mensagem in websocket:

            print(
                f"Jogador {jogador}: {mensagem}"
            )

            try:

                dados = json.loads(mensagem)

                # ==================================================
                # MOVIMENTO DA RAQUETE
                # ==================================================

                if dados["tipo"] == "raquete":

                    if jogador == 1:

                        player1_y = dados["y"]

                    elif jogador == 2:

                        player2_y = dados["y"]

                    # Envia para o outro jogador
                    for numero, outro_jogador in jogadores.items():

                        if numero != jogador:

                            try:

                                await outro_jogador.send(
                                    mensagem
                                )

                            except websockets.exceptions.ConnectionClosed:

                                pass

                # ==================================================
                # JOGAR NOVAMENTE
                # ==================================================

                elif dados["tipo"] == "reiniciar":

                    print(
                        f"Jogador {jogador} "
                        f"está pronto para jogar novamente."
                    )

                    # Adiciona jogador à lista de prontos
                    jogadores_prontos.add(jogador)

                    # ==================================================
                    # AVISA QUE ESTÁ ESPERANDO
                    # ==================================================

                    for jogador_atual in list(
                        jogadores.values()
                    ):

                        try:

                            await jogador_atual.send(
                                f"AGUARDANDO_REINICIO:{jogador}"
                            )

                        except websockets.exceptions.ConnectionClosed:

                            pass

                    # ==================================================
                    # OS DOIS JOGADORES ESTÃO PRONTOS
                    # ==================================================

                    if len(jogadores_prontos) == 2:

                        print(
                            "Os dois jogadores estão prontos!"
                        )

                        # Zera o placar
                        player1_score = 0
                        player2_score = 0

                        # Reseta as raquetes
                        player1_y = 200
                        player2_y = 200

                        # Reseta a bola
                        ball_x = 390
                        ball_y = 240

                        # Reseta velocidade
                        ball_speed_x = 4
                        ball_speed_y = 4

                        # Libera a partida
                        game_over = False

                        # Limpa a lista
                        jogadores_prontos.clear()

                        print(
                            "Nova partida iniciada!"
                        )

                        # ==================================================
                        # AVISA OS DOIS JOGADORES
                        # ==================================================

                        for jogador_atual in list(
                            jogadores.values()
                        ):

                            try:

                                await jogador_atual.send(
                                    "NOVA_PARTIDA"
                                )

                                await jogador_atual.send(
                                    "PLACAR:0,0"
                                )

                                await jogador_atual.send(
                                    "390,240"
                                )

                            except websockets.exceptions.ConnectionClosed:

                                pass

            except (
                json.JSONDecodeError,
                KeyError
            ):

                pass

    except websockets.exceptions.ConnectionClosed:

        print(
            f"Jogador {jogador} desconectou!"
        )

    finally:

        if jogador in jogadores:

            del jogadores[jogador]

        # Remove da lista de prontos
        jogadores_prontos.discard(jogador)

        print(
            f"Jogadores conectados: "
            f"{len(jogadores)}"
        )

        # ==================================================
        # QUANDO TODOS SAEM
        # ==================================================

        if len(jogadores) == 0:

            player1_score = 0
            player2_score = 0

            ball_x = 390
            ball_y = 240

            ball_speed_x = 4
            ball_speed_y = 4

            game_over = False

            jogadores_prontos.clear()

            print(
                "Partida encerrada. "
                "Placar zerado."
            )


# ==================================================
# ATUALIZAÇÃO DA BOLA
# ==================================================

async def atualizar_bola():

    global ball_x
    global ball_y

    global ball_speed_x
    global ball_speed_y

    global player1_score
    global player2_score

    global game_over

    while True:

        # Só movimenta a bola quando:
        # existem dois jogadores
        # e a partida não terminou

        if len(jogadores) == 2 and not game_over:

            # ==================================================
            # MOVIMENTO
            # ==================================================

            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # ==================================================
            # TETO
            # ==================================================

            if ball_y <= 0:

                ball_y = 0

                ball_speed_y *= -1

            # ==================================================
            # CHÃO
            # ==================================================

            if ball_y >= 480:

                ball_y = 480

                ball_speed_y *= -1

            # ==================================================
            # RAQUETE JOGADOR 1
            # ==================================================

            if (
                ball_x <= 32
                and ball_y + 20 >= player1_y
                and ball_y <= player1_y + 100
                and ball_speed_x < 0
            ):

                ball_speed_x *= -1

                ball_x = 32

                print(
                    "Bola bateu na "
                    "raquete do Jogador 1!"
                )

            # ==================================================
            # RAQUETE JOGADOR 2
            # ==================================================

            if (
                ball_x + 20 >= 768
                and ball_y + 20 >= player2_y
                and ball_y <= player2_y + 100
                and ball_speed_x > 0
            ):

                ball_speed_x *= -1

                ball_x = 748

                print(
                    "Bola bateu na "
                    "raquete do Jogador 2!"
                )

            # ==================================================
            # JOGADOR 2 MARCOU
            # ==================================================

            if ball_x < 0:

                player2_score += 1

                print(
                    f"Jogador 2 marcou! "
                    f"Placar: "
                    f"{player1_score} x "
                    f"{player2_score}"
                )

                # Jogador 2 venceu
                if player2_score >= 5:

                    game_over = True

                    print(
                        "Jogador 2 venceu!"
                    )

                else:

                    ball_x = 390
                    ball_y = 240

                    ball_speed_x = 4
                    ball_speed_y = 4

            # ==================================================
            # JOGADOR 1 MARCOU
            # ==================================================

            if ball_x > 780:

                player1_score += 1

                print(
                    f"Jogador 1 marcou! "
                    f"Placar: "
                    f"{player1_score} x "
                    f"{player2_score}"
                )

                # Jogador 1 venceu
                if player1_score >= 5:

                    game_over = True

                    print(
                        "Jogador 1 venceu!"
                    )

                else:

                    ball_x = 390
                    ball_y = 240

                    ball_speed_x = -4
                    ball_speed_y = 4

            # ==================================================
            # ENVIA BOLA
            # ==================================================

            mensagem = (
                f"{ball_x},{ball_y}"
            )

            # ==================================================
            # ENVIA PLACAR
            # ==================================================

            mensagem_placar = (
                f"PLACAR:"
                f"{player1_score},"
                f"{player2_score}"
            )

            # ==================================================
            # ENVIA PARA OS DOIS JOGADORES
            # ==================================================

            for jogador in list(
                jogadores.values()
            ):

                try:

                    await jogador.send(
                        mensagem
                    )

                    await jogador.send(
                        mensagem_placar
                    )

                    # ==================================================
                    # AVISA O VENCEDOR
                    # ==================================================

                    if game_over:

                        if player1_score >= 5:

                            await jogador.send(
                                "VENCEDOR:1"
                            )

                        elif player2_score >= 5:

                            await jogador.send(
                                "VENCEDOR:2"
                            )

                except websockets.exceptions.ConnectionClosed:

                    pass

        # Aproximadamente 60 atualizações por segundo
        await asyncio.sleep(0.016)


# ==================================================
# SERVIDOR
# ==================================================

async def main():

    servidor = await websockets.serve(

        conectar,

        # Permite acesso pela rede local
        "0.0.0.0",

        8080
    )

    print(
        "Servidor WebSocket iniciado!"
    )

    print(
        "Rodando na porta 8080"
    )

    print(
        "Aguardando jogadores..."
    )

    # Inicia atualização da bola
    asyncio.create_task(
        atualizar_bola()
    )

    # Mantém servidor funcionando
    await servidor.wait_closed()


# ==================================================
# INICIA O SERVIDOR
# ==================================================

asyncio.run(main())