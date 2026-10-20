# Sistema de Controle de Acesso — IFF

Protótipo de reconhecimento facial para controle de acesso desenvolvido para o **Instituto Federal Fluminense (IFF)**. O sistema captura imagens da webcam em tempo real, detecta rostos, gera *embeddings* faciais e os compara contra um banco de dados local para autorizar ou negar o acesso de pessoas cadastradas.

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Executando o sistema](#executando-o-sistema)
  - [Cadastrando uma pessoa](#cadastrando-uma-pessoa)
  - [Reconhecimento em tempo real](#reconhecimento-em-tempo-real)
  - [Atalhos de teclado](#atalhos-de-teclado)
- [Como funciona o reconhecimento](#como-funciona-o-reconhecimento)
- [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
- [Modelos de IA](#modelos-de-ia)
- [Observações](#observações)

## Visão Geral

O sistema realiza o ciclo completo de reconhecimento facial diretamente na máquina local, sem enviar dados para serviços externos. Ele é dividido em duas operações principais:

1. **Cadastro** — captura o rosto de uma pessoa pela câmera, gera um *embedding* facial e armazena nome, matrícula e vetor no banco SQLite.
2. **Identificação** — em tempo real, detecta rostos no vídeo, gera o *embedding* e compara com os vetores cadastrados usando similaridade de cosseno. Se a similaridade ultrapassa um limiar, o acesso é autorizado e os dados da pessoa são exibidos.

## Funcionalidades

- Captura de vídeo ao vivo pela webcam com espelhamento visual
- Detecção facial em tempo real com *bounding boxes*
- Cadastro de usuários com nome e matrícula
- Reconhecimento facial por similaridade de cosseno
- Indicação visual de estados: aguardando, autorizado, não identificado e múltiplos rostos
- Persistência local em SQLite (sem dependência de serviços na nuvem)
- Interface moderna com CustomTkinter
- Suporte a tela cheia

## Arquitetura

```
app.py                       Ponto de entrada — inicializa a janela principal
│
├── ui/                      Camada de interface (CustomTkinter)
│   ├── main_window.py       Janela principal: câmera, reconhecimento e status
│   └── register_window.py   Janela de cadastro de novas pessoas
│
├── vision/                  Camada de visão computacional
│   ├── camera.py            Captura de frames via OpenCV
│   ├── detector.py          Detecção facial com MediaPipe BlazeFace
│   ├── embedder.py          Geração de embeddings com MobileFaceNet (TFLite)
│   └── recognizer.py        Comparação por similaridade de cosseno
│
├── database/                Camada de persistência
│   └── database.py          SQLite — armazena usuários e embeddings
│
├── services/                Camada de serviços (reservada para lógica de negócio)
│   ├── access_control.py
│   └── registration.py
│
├── models/                  Modelos TFLite
│   ├── blaze_face_short_range.tflite   Detecção facial
│   └── mobilefacenet.tflite            Geração de embeddings
│
└── assets/                  Recursos visuais
    └── iff_logo.png         Logo do IFF exibida no cabeçalho
```

### Fluxo de dados

```
Webcam → Camera.read() → FaceDetector.detect() → FaceEmbedder.generate() → FaceRecognizer.recognize() → Database.get_users()
                                                                                                            ↓
                                                                                               Interface (autorizado / não identificado)
```

## Tecnologias

| Tecnologia | Função |
|------------|--------|
| [OpenCV](https://opencv.org/) | Captura de vídeo e manipulação de imagens |
| [MediaPipe](https://mediapipe.dev/) | Detecção facial (BlazeFace) |
| [TensorFlow Lite](https://www.tensorflow.org/lite) | Inferência do MobileFaceNet para embeddings |
| [NumPy](https://numpy.org/) | Operações vetoriais e similaridade |
| [Pillow](https://python-pillow.org/) | Conversão de imagens para a interface |
| [CustomTkinter](https://customtkinter.tomschimansky.com/) | Interface gráfica moderna |
| [SQLite](https://www.sqlite.org/) | Armazenamento local dos usuários |

## Pré-requisitos

- Python 3.9 ou superior
- Uma webcam conectada e acessível

## Instalação

1. Clone o repositório (ou descompacte o projeto) e acesse a pasta:

```bash
cd reconhecimento-facial
```

2. Crie e ative um ambiente virtual:

```bash
# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Certifique-se de que os modelos TFLite estejam presentes na pasta `models/`:

```
models/
├── blaze_face_short_range.tflite
└── mobilefacenet.tflite
```

> **Importante:** os arquivos `.tflite` são ignorados pelo `.gitignore`. Se o projeto foi clonado, será necessário obter os modelos separadamente (veja [Modelos de IA](#modelos-de-ia)).

## Uso

### Executando o sistema

```bash
python app.py
```

A janela principal abre com o feed da câmera à esquerda e o painel de identificação à direita.

### Cadastrando uma pessoa

1. Clique no botão **+ CADASTRAR PESSOA** no painel direito.
2. Na janela de cadastro, preencha **nome completo** e **matrícula**.
3. Posicione o rosto centralizado diante da câmera (apenas uma pessoa por vez).
4. Quando o status indicar "✓ Rosto detectado", clique em **CAPTURAR E CADASTRAR**.
5. Uma mensagem de confirmação será exibida e o usuário estará disponível para reconhecimento.

### Reconhecimento em tempo real

Com a janela principal aberta, basta posicionar uma pessoa diante da câmera. O sistema:

- Detecta o rosto e desenha a *bounding box*.
- A cada 10 frames, gera o *embedding* e compara com os cadastrados.
- Exibe o resultado no painel direito:
  - **ACESSO AUTORIZADO** (verde) — pessoa reconhecida, mostra nome e matrícula.
  - **NÃO IDENTIFICADO** (vermelho) — nenhuma correspondência acima do limiar.
  - **MÚLTIPLOS ROSTOS** (laranja) — mais de uma pessoa no enquadramento.
  - **AGUARDANDO IDENTIFICAÇÃO** — nenhum rosto detectado.

### Atalhos de teclado

| Tecla | Ação |
|-------|------|
| `F11` | Alterna tela cheia |
| `ESC` | Sai da tela cheia |

## Como funciona o reconhecimento

1. **Detecção** — o frame BGR do OpenCV é convertido para RGB e processado pelo BlazeFace (`blaze_face_short_range.tflite`) via MediaPipe, retornando *bounding boxes* e confianças. A confiança mínima é 0,6.
2. **Recorte** — o rosto é recortado com uma margem de 20% ao redor da *bounding box* para incluir contexto.
3. **Embedding** — o recorte é redimensionado, normalizado para o intervalo `[-1, 1]` e processado pelo MobileFaceNet (`mobilefacenet.tflite`), gerando um vetor de características. Esse vetor é normalizado por L2.
4. **Comparação** — a similaridade de cosseno é calculada entre o embedding da captura e todos os embeddings armazenados no banco. O melhor resultado é comparado ao **limiar de 0,65**:
   - `similaridade >= 0,65` → usuário reconhecido (acesso autorizado).
   - Caso contrário → não identificado.

## Estrutura do Banco de Dados

O sistema usa SQLite, armazenado em `database/iff_access.db`. A tabela `users`:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER PK | Identificador único |
| `name` | TEXT | Nome completo |
| `registration_number` | TEXT UNIQUE | Matrícula |
| `embedding` | BLOB | Vetor de embedding em `float32` |
| `created_at` | DATETIME | Data/hora de cadastro |

## Modelos de IA

Os modelos ficam na pasta `models/` e não são versionados (ignorados pelo `.gitignore` por serem arquivos binários). São necessários para o funcionamento:

- **`blaze_face_short_range.tflite`** — detector de rostos do MediaPipe, otimizado para rostos próximos. Disponível no [MediaPipe Models](https://developers.google.com/mediapipe/solutions/vision/face_detector).
- **`mobilefacenet.tflite`** — gerador de *embeddings* faciais baseado no MobileFaceNet, que produz vetores de características para comparação.

Coloque ambos os arquivos na pasta `models/` antes de executar o sistema.

## Observações

- O sistema é um **protótipo** voltado para fins acadêmicos de demonstração de reconhecimento facial e não deve ser usado como único mecanismo de controle de acesso em ambientes de produção sem validações adicionais de segurança.
- O reconhecimento é feito inteiramente *on-device*; nenhuma imagem ou dado biométrico é enviado a serviços externos.
- O limiar de similaridade (0,65) pode ser ajustado em `vision/recognizer.py` para equilibrar falsos positivos e falsos negativos conforme a necessidade.
- A pasta `services/` está reservada para futura extração da lógica de negócio (controle de acesso e registro de eventos) fora da camada de interface.
