Ambiente de IA Local com Docker
Este repositório contém uma configuração Docker completa para rodar um ambiente de desenvolvimento de IA localmente. O ambiente inclui:

n8n: Uma ferramenta de automação de fluxo de trabalho para conectar APIs.

PostgreSQL: Um banco de dados para o n8n e outras aplicações.

Ollama: Um servidor para executar modelos de linguagem (LLMs) localmente.

Open WebUI: Uma interface de chat amigável para interagir com os modelos do Ollama.

Pré-requisitos
Para executar este ambiente, você precisa ter o Docker Desktop instalado em sua máquina.

Docker Desktop

Como Começar
1. Configure o Ambiente
Primeiro, crie um arquivo chamado docker-compose.yml em uma pasta de sua escolha e adicione o seguinte conteúdo. Este arquivo define todos os serviços e como eles se comunicam.

2. Inicie os Serviços
Abra o terminal na mesma pasta onde você salvou o arquivo docker-compose.yml e execute o comando:

Bash

docker-compose up -d

Este comando irá:

Baixar as imagens necessárias (n8n, postgres, ollama, open-webui).

Criar uma rede interna para todos os serviços.

Iniciar os contêineres na ordem correta, garantindo que o PostgreSQL e o Ollama estejam prontos antes do n8n e do Open WebUI.

Baixar o modelo llama3 para o Ollama.

3. Acesse a Interface
Aguarde alguns minutos para que todos os serviços subam e os modelos sejam baixados. Em seguida, acesse as interfaces no seu navegador:

n8n: http://localhost:5678

Open WebUI: http://localhost:3000

Observações Importantes
Persistência de Dados: Todos os serviços usam volumes para armazenar seus dados em pastas locais (./data). Isso garante que suas configurações, modelos e histórico de chat não sejam perdidos ao reiniciar os contêineres.

GPU: O serviço ollama está configurado para usar sua GPU, caso você tenha uma NVIDIA com o NVIDIA Container Toolkit instalado.

Portas: Se as portas 5678 ou 3000 estiverem em uso, você pode alterá-las no arquivo docker-compose.yml. Por exemplo, para 5679:5678.

Limpeza: Para parar os serviços, use docker-compose stop. Para parar e remover os contêineres e a rede (mas manter os volumes), use docker-compose down.
