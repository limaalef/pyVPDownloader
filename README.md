# VP Downloader 🎬

Ferramenta Python para download de vídeos em streaming usando N_m3u8DL-RE, com interface interativa e suporte a navegação por teclado.

## ✨ Características

- 🎮 **Interface interativa** com navegação por setas do teclado
- 📺 **Lista de canais** pré-configurada e personalizável (YAML)
- 🔐 **Gerenciamento seguro** de credenciais usando keyring do sistema
- 📅 **Seletor de data/hora** visual para gravações DVR
- ⚙️ **Menu de configurações** completo
- 🖥️ **Multiplataforma** (Windows, macOS, Linux)
- 🔄 **Modo CLI** para automação


## 📊 Estrutura do Projeto

```
pyVPDownloader/
├── vpdownloader.py       # Programa
├── requirements.txt      # Dependências Python
├── README.md             
├── mp4decrypt.exe        # (Download obrigatório) Executável local
├── N_m3u8DL-RE.exe       # (Download obrigatório) Executável local
├── INSTALL.cmd           # Instalação facilitada de dependências
└── START.cmd             # Inicialização facilitada do programa
```

## 📋 Requisitos

### Ferramentas Externas
- **N_m3u8DL-RE** - [Download aqui](https://github.com/nilaoda/N_m3u8DL-RE/releases)
- **mp4decrypt** - [Download aqui](https://www.bento4.com/downloads/)
  - Devem estar no PATH do sistema ou na pasta do script

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/limaalef/pyVPDownloader.git
cd git clone https://github.com/limaalef/pyVPDownloader.git
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

ou execute INSTALL.cmd (para Windows)

3. **Baixe o N_m3u8DL-RE:**
   - Windows: Baixe `N_m3u8DL-RE.exe` e `mp4decrypt` e coloque na pasta do projeto ou no PATH
   - Linux/macOS: Instale via package manager ou coloque na pasta do projeto

## 📖 Modo de Uso

### Modo Interativo

Execute sem argumentos para abrir o menu interativo:
```bash
python vpdownloader.py
```
ou execute START.cmd (para Windows)

**Navegação:**
- `↑` `↓` - Move entre linhas
- `←` `→` - Move entre colunas
- `Enter` - Seleciona canal
- `ESC` - Cancela
- `90` - Inserir nome do canal manualmente
- `98` - Inserir URL manualmente
- `99` - Acessar configurações

### Modo Linha de Comando

**Download ao vivo:**
```bash
python vpdownloader.py espn
```

**Download DVR (período específico):**
```bash
python vpdownloader.py espn --start 202501061200 --end 202501061400
```

**URL manual com chave:**
```bash
python vpdownloader.py "https://exemplo.com/video.m3u8" --key "abc123:def456"
```

**Especificar formato:**
```bash
python vpdownloader.py sportv
```

## ⚙️ Configuração

### Arquivos de Configuração

Os arquivos são salvos em:
- **Windows:** `%LOCALAPPDATA%\VideoDownloader\`
- **macOS:** `~/Library/Application Support/VideoDownloader/`
- **Linux:** `~/.config/VideoDownloader/`

**Arquivos criados:**
- `config.json` - Configurações do programa
- `channels.yaml` - Lista de canais disponíveis
- `downloader.log` - Log de operações
- `keychain.txt` - Histórico de chaves utilizadas

### Personalizar Canais

Edite `channels.yaml`:
```yaml
channels:
  - id: 0
    name: "canal1"
  - id: 1
    name: "canal2"
  - id: 2
    name: "canal3"
```

### Opções de Configuração

Acesse o menu com `99` no modo interativo ou edite `config.json`:

```json
{
  "download_path": "C:/Users/Usuario/Downloads",
  "output_format": "mp4",
  "show_command": false,
  "show_progress": true,
  "delete_temp": true,
  "api_url": "<URL DA API>"
}
```

## 🎯 Funcionalidades

### Seletor de Data/Hora
- Navegue com `←` `→` entre campos (dia/mês/ano/hora/minuto)
- Use `↑` `↓` para ajustar valores
- Validação automática de datas (7 dias para trás)
- Suporte a anos bissextos

### Gerenciamento de Credenciais
- Armazenamento seguro usando keyring do sistema
- Opções para alterar ou remover credenciais
- Solicitação automática no primeiro uso


## 🐛 Solução de Problemas

### N_m3u8DL-RE não encontrado
```bash
# Verifique se está no PATH
N_m3u8DL-RE --version

# Ou coloque na mesma pasta do script
```

### Erro de credenciais
```bash
# Remova credenciais salvas e tente novamente
# Opção 99 > Gerenciar credenciais > Remover
```

### Erro de permissão no Linux/macOS
```bash
chmod +x N_m3u8DL-RE