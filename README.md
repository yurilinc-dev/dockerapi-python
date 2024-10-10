# Docker Event Monitoring Script

Este projeto monitora eventos de contêiner Docker e envia notificações para um canal do Discord quando um contêiner é finalizado. O monitoramento é feito através da API do Docker e o envio de notificações é realizado via Webhook do Discord.

## Requisitos

Antes de começar, você precisará dos seguintes requisitos:

- Python 3.7+ instalado
- Docker instalado e configurado para permitir acesso remoto via TCP (porta 2375)
- Um Webhook do Discord configurado
- Dependências Python (listadas abaixo)

### Pré-requisitos

1. **Instalar Python 3:**

   Certifique-se de que o Python 3 está instalado. Execute o seguinte comando no terminal:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Instalar Docker:**

   Se o Docker ainda não estiver instalado no seu sistema Linux, instale-o com os seguintes comandos:

   ```bash
   sudo apt update
   sudo apt install docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

   Verifique se o Docker está funcionando corretamente:

   ```bash
   sudo docker --version
   ```

3. **Configurar Docker para acesso via TCP:**

   O script utiliza a API do Docker via TCP (porta 2375). Para configurar o Docker para ouvir nessa porta:

   - Edite o arquivo de configuração do Docker:

     ```bash
     sudo nano /lib/systemd/system/docker.service
     ```

   - Substitua a linha `ExecStart` para permitir conexões via TCP:

     ```bash
     ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 --containerd=/run/containerd/containerd.sock
     ```

   - Recarregue o systemd e reinicie o serviço Docker:

     ```bash
     sudo systemctl daemon-reload
     sudo systemctl restart docker
     ```

   - Certifique-se de que o Docker está escutando na porta 2375:

     ```bash
     sudo netstat -lntp | grep dockerd
     ```

## Configuração do Projeto

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/yurilinc-dev/dockerapi-python.git
   cd dockerapi-python
   ```

2. **Instalar dependências Python:**

   Use `pip` para instalar as dependências necessárias:

   ```bash
   pip3 install -r requirements.txt
   ```

   O arquivo `requirements.txt` deve conter:
   ```
   docker
   datetime
   requests
   logging
   time
   os
   dotenv
   ```

3. **Configuração de variáveis de ambiente (.env):**

   Crie um arquivo `.env` no diretório do projeto com as seguintes variáveis:

   ```
   CHANNEL_ID=1316156465413131654
   WEBHOOK_ID=w_2_eRN4_UNIbKKU16f07vp0IsIM_v81ofN88jwbp
   IP=127.0.0.1
   PORT=2375
   ```

   O `CHANNEL_ID` e `WEBHOOK_ID` são valores fornecidos pelo webhook do Discord.
   O `IP` e `PORT` são valores fornecidos conforme a configuração do Docker file para API.

## Como Executar

1. **Iniciar o monitoramento de eventos do Docker:**

   Para iniciar o script e monitorar os eventos Docker, basta executar o seguinte comando:

   ```bash
   python3 events.py
   ```

   O script começará a monitorar eventos de finalização de contêineres (quando um contêiner "morre") e enviará uma mensagem de notificação para o Discord com o ID e o nome do contêiner.

### Exemplo de saída:

```
INFO:root:Payload: {'content': 'O container my_container (c19d4f5d2a5f) foi finalizado às 2024-10-10 14:22:10'}
INFO:root:Falha ao enviar webhook: 204 - No Content
```

Isso indica que a notificação foi enviada com sucesso para o Discord.

## Resolução de Problemas

1. **Docker não está respondendo via TCP:**

   - Certifique-se de que a configuração da porta 2375 está correta e o Docker está escutando nessa porta:

     ```bash
     sudo netstat -lntp | grep dockerd
     ```

2. **Erro ao enviar webhook:**

   - Verifique o status do webhook no Discord e valide se o `CHANNEL_ID` e o `WEBHOOK_ID` estão corretos no arquivo `.env`.

3. **Reinstalação do Docker:**

   Caso haja algum problema crítico com o Docker, você pode reinstalá-lo com os seguintes comandos:

   ```bash
   sudo apt remove docker docker-engine docker.io containerd runc
   sudo apt install docker.io
   ```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
