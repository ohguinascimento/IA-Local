<<<<<<< HEAD
# IA Local: Geração de Vídeo e LLMs com Docker

Este repositório contém um ambiente completo de Inteligência Artificial rodando localmente via **Docker**, otimizado para placas com **6 GB de VRAM (NVIDIA GeForce RTX 2060)** e **32 GB de RAM**.

---

## 🚀 Serviços Disponíveis

| Serviço | Função | Porta / URL Local |
| :--- | :--- | :--- |
| **ComfyUI** | Geração e Animação de Vídeos e Imagens (AnimateDiff, Wan 2.1, LTX-Video) | [http://localhost:8188](http://localhost:8188) |
| **Open WebUI** | Interface Web amigável de chat para modelos de linguagem | [http://localhost:3001](http://localhost:3001) |
| **Ollama** | Servidor de LLMs (Llama 3, Qwen 2.5 Coder, etc.) | [http://localhost:11434](http://localhost:11434) |

---

## 🛠️ Pré-requisitos
* **Docker Desktop** rodando com suporte a GPU NVIDIA ativado (WSL2).
* Drivers da NVIDIA atualizados.

---

## 📁 Estrutura do Repositório

```text
ia-local/
├── docker-compose.yml          # Definição dos containers (Ollama, Open WebUI e ComfyUI)
├── .gitignore                  # Ignora modelos pesados e vídeos gerados no git
├── README.md                   # Guia de uso
├── scripts/
│   └── download_models.ps1     # Script facilitador para baixar os modelos de vídeo
├── storage/
│   └── comfyui/
│       ├── models/             # Checkpoints, AnimateDiff, VAE, LoRAs
│       ├── custom_nodes/       # Extensões e nós customizados do ComfyUI
│       ├── input/              # Imagens/vídeos de entrada (Image-to-Video)
│       └── output/             # Onde seus vídeos e animações gerados são salvos!
└── workflows/
    └── animatediff_basic_txt2vid.json  # Workflow inicial de Texto para Vídeo
```

---

## 🎬 Passo a Passo: Geração de Vídeo com ComfyUI

### Passo 1: Baixar os Modelos Iniciais
Para rodar na RTX 2060 (6 GB), o modelo mais estável e rápido é o **AnimateDiff (SD 1.5)**.
Execute no PowerShell para baixar o checkpoint DreamShaper 8 e o módulo de movimento:

```powershell
.\scripts\download_models.ps1
```
*(Selecione a opção `1` para o AnimateDiff Pack).*

Ou você pode baixar manualmente e colocar nas seguintes pastas:
* `storage/comfyui/models/checkpoints/` -> `DreamShaper_8_pruned.safetensors`
* `storage/comfyui/models/animatediff_models/` -> `mm_sd_v15_v2.ckpt`

---

### Passo 2: Iniciar o ComfyUI

Para iniciar apenas o ambiente de vídeo:
```bash
docker compose up -d comfyui
```

Para iniciar todos os serviços (Ollama + Open WebUI + ComfyUI):
```bash
docker compose up -d
```

> **Dica de Memória:** O arquivo `docker-compose.yml` está configurado com `OLLAMA_KEEP_ALIVE=0`. Isso faz com que o Ollama libere a memória de vídeo imediatamente após terminar uma resposta, deixando 100% dos 6 GB de VRAM livres para a renderização dos vídeos no ComfyUI.

---

### Passo 3: Abrir a Interface e Instalar os Nós de Vídeo
1. Acesse no navegador: **[http://localhost:8188](http://localhost:8188)**.
2. Na barra lateral direita do ComfyUI, clique em **Manager**.
3. Clique em **Install Custom Nodes** e instale:
   * **ComfyUI-AnimateDiff-Evolved** (Necessário para a animação do AnimateDiff).
   * **ComfyUI-VideoHelperSuite** (Opcional, para exportar vídeos em formato MP4 com áudio).
4. Clique no botão **Restart** que o ComfyUI solicitar para recarregar as extensões.

---

### Passo 4: Carregar o Workflow de Vídeo
1. Abra a pasta `workflows/` deste repositório no seu computador.
2. **Arraste e solte** o arquivo `animatediff_basic_txt2vid.json` diretamente para dentro da janela do ComfyUI no navegador.
3. No nó `CLIPTextEncode` verde (positivo), digite o prompt do que deseja criar.
4. Clique em **Queue Prompt** (ou aperte `Ctrl + Enter`).
5. O vídeo será gerado e ficará salvo automaticamente na pasta `storage/comfyui/output/`!

---

## 💡 Dicas para Renderização em 6 GB de VRAM

| Configuração | Recomendação para 6 GB | Motivo |
| :--- | :--- | :--- |
| **Resolução** | `512x512` ou `512x768` | Resoluções maiores (como 1024x1024) exigem upscaling via tile para não estourar a VRAM. |
| **Número de Frames** | `16` a `32` frames | 16 frames a 8 fps = 2 segundos de vídeo fluído e rápido. |
| **Passos (Steps)** | `20` a `25` passos | Suficiente para qualidade excelente sem sobrecarregar a GPU. |
| **Modelos Modernos (Wan 2.1 / LTX-Video)** | Usar quantizações **GGUF (Q4 / Q5)** | Graças aos seus 32 GB de RAM, o ComfyUI faz offload suave entre a RAM e a VRAM. |

---

## 🛑 Parando os Serviços

Para pausar os containers e liberar memória:
```bash
docker compose stop
```
Ou para remover os containers mantendo os arquivos intactos:
```bash
docker compose down
```

=======
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
>>>>>>> d9ce7e6e222890389962cebb93c63775b8c5addc
