"""
Video Downloader - Download de vídeos com N_m3u8DL-RE
Versão Python baseada no Vivo Play Downloader
"""

import os
import re
import sys
import json
import base64
import logging
import argparse
import math
import platform
import shutil
import subprocess
import traceback
import linecache
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, List

import yaml
import requests
import keyring

# Configurações do sistema
SYSTEM = platform.system()
TERMINAL_SIZE = shutil.get_terminal_size().columns
TITULO = "Vivo Play Downloader"
VERSION = "1.0.1"

# Para navegação por teclado
if SYSTEM == "Windows":
    import msvcrt
else:
    import tty
    import termios


class Colors:
    """Códigos ANSI para cores"""
    import shutil
    from typing import List, Optional
    import math

    # Cores primárias
    PRIMARY_TEXT_COLOR = "\033[38;2;205;214;244m"
    SECONDARY_TEXT_COLOR = "\033[38;2;221;148;226m"
    SUCCESS_COLOR = "\033[92m"
    ERROR_COLOR = "\033[91m"
    WARNING_COLOR = "\033[93m"
    INFO_COLOR = "\033[94m"
    LINE_COLOR = "\033[38;2;54;54;84m"

    # Cores de destaque
    HIGHLIGHTED_COLOR = "\033[38;2;245;237;194m"
    UNHIGHLIGHTED_COLOR = "\033[38;2;162;169;193m"
    SELECTED_BG = "\033[45m\033[97m\033[1m"

    # Cores de fundo
    BG_COLOR = "\033[48;2;30;30;46m"  #'\033[40m' Preto
    MAGENTA_BG = "\033[45m"

    # Formatação
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[40m"

    # Atalhos combinados
    TITLE = "\033[1m\033[95m"
    PROMPT = "\033[1m\033[96m"

    # Medidas
    MARGIN_LEFT = 4

    # Bordas
    HORIZONTAL = '─'
    VERTICAL = '│'
    TOP_LEFT = '╭'
    TOP_RIGHT = '╮'
    TOP_MIDDLE = '┬'
    BOTTOM_LEFT = '╰'
    BOTTOM_RIGHT = '╯'
    BOTTOM_MIDDLE = '┴'
    VERTICAL_LEFT = '├'

    def clear_screen():
        """Limpa a tela"""
        print(f"{Colors.BG_COLOR}")
        os.system("cls" if SYSTEM == "Windows" else "clear")

    def print_banner(title=TITULO, subtitle: Optional[str] = "", version: Optional[str] = VERSION):
        """Exibe banner do programa"""
        Colors.clear_screen()
        cols = shutil.get_terminal_size().columns

        # Linha 1
        Colors.item()
        Colors.center_text(title, Colors.SECONDARY_TEXT_COLOR)

        # Linha 2
        Colors.item()

        # Linha 3
        Colors.center_text(f"v{version}     @limaalef", highlight=version)
    
    def error(message, title = "Erro"):
        Colors._box(title, message, Colors.ERROR_COLOR, center=True)

    def warning(message, title = "Atenção"):
        Colors._box(title, message, Colors.WARNING_COLOR, center=True)

    def info(message, title = "Info"):
        Colors._box(title, message, Colors.INFO_COLOR, center=True)

    def ok(message, title = "Ok"):
        Colors._box(title, message, Colors.SUCCESS_COLOR, center=True)

    def item(title: str = "", subtitle: Optional[str] = "", index: Optional[str] = "", color = PRIMARY_TEXT_COLOR, highlight: Optional[str] = ""):
        left_margin = Colors.MARGIN_LEFT
        padding = " " * left_margin

        if highlight and highlight in title:
            split_title = title.split(highlight)
            title = f"{split_title[0]}{Colors.HIGHLIGHTED_COLOR}{highlight}{Colors.PRIMARY_TEXT_COLOR}{split_title[1]}"

        if subtitle:
            line = f"{color}{title}: {Colors.SECONDARY_TEXT_COLOR}{subtitle}{Colors.PRIMARY_TEXT_COLOR}"
        else:
            line = f"{color}{title} {Colors.SECONDARY_TEXT_COLOR}{subtitle}{Colors.PRIMARY_TEXT_COLOR}"

        if index:
            line = f"{Colors.HIGHLIGHTED_COLOR}{index} {line}"
    
        line = f"{padding}{line}"
        print(line)

    def select_item(title: str = "", selected: str = ""):
        indent = " " * Colors.MARGIN_LEFT

        if selected:
            output = f"{Colors.PRIMARY_TEXT_COLOR}{indent}{title} {Colors.UNHIGHLIGHTED_COLOR}[{selected}]{Colors.PRIMARY_TEXT_COLOR}: {Colors.HIGHLIGHTED_COLOR}"
        else:
            output = f"{Colors.PRIMARY_TEXT_COLOR}{indent}{title}: {Colors.HIGHLIGHTED_COLOR}"

        return output

    def center_text(title: str = "", color: str = PRIMARY_TEXT_COLOR, highlight: Optional[str] = ""):
        total_width = shutil.get_terminal_size().columns
        if TERMINAL_SIZE < total_width and TERMINAL_SIZE > 0:
            total_width = TERMINAL_SIZE
            
        size = total_width
        
        if highlight and highlight in title:
            split_title = title.split(highlight)
            title = f"{split_title[0]}{Colors.HIGHLIGHTED_COLOR}{highlight}{color}{split_title[1]}"
            size = size + len(Colors.HIGHLIGHTED_COLOR) + len(color)

        line = title.center(size)
        print(f"{color}{line}{Colors.PRIMARY_TEXT_COLOR}")

    def center_title(title: str = "", color: str = PRIMARY_TEXT_COLOR, highlight: Optional[str] = ""):
        total_width = shutil.get_terminal_size().columns
        if TERMINAL_SIZE < total_width and TERMINAL_SIZE > 0:
            total_width = TERMINAL_SIZE

        left_margin = Colors.MARGIN_LEFT
        max_width = total_width - left_margin*2 - 2

        line_width = math.floor((max_width - len(title))/2)
        line_item = f"─" * line_width

        padding = " " * left_margin
        
        if highlight and highlight in title:
            split_title = title.split(highlight)
            title = f"{split_title[0]}{Colors.HIGHLIGHTED_COLOR}{highlight}{Colors.PRIMARY_TEXT_COLOR}{split_title[1]}"

        line = f"{padding}{Colors.LINE_COLOR}{line_item} {Colors.SECONDARY_TEXT_COLOR}{title} {Colors.LINE_COLOR}{line_item}{Colors.PRIMARY_TEXT_COLOR}"
        print(f"\n{color}{line}\n")
        
    def list_item(items: list[str]):
        left_margin = Colors.MARGIN_LEFT
        total_width = shutil.get_terminal_size().columns
        if TERMINAL_SIZE < total_width and TERMINAL_SIZE > 0:
            total_width = TERMINAL_SIZE

        max_width = total_width - left_margin * 2 - 2 - 2
        padding = " " * left_margin
        s_padding = Colors.HORIZONTAL * 2

        for i, item in enumerate(items):
            item_lines = Colors._wrap_text(item, max_width)
            for k, line_text in enumerate(item_lines):
                if len(items) == 1:
                    if k == 0:
                        prefix = f"{padding}{Colors.LINE_COLOR}{Colors.BOTTOM_LEFT}{s_padding} "
                    else:
                        prefix = f"{padding}    "
                else:
                    if i == len(items) - 1:
                        if k == 0:
                            prefix = f"{padding}{Colors.LINE_COLOR}{Colors.BOTTOM_LEFT}{s_padding} "
                        else:
                            prefix = f"{padding}{Colors.LINE_COLOR}    "
                    else:
                        if k == 0:
                            prefix = f"{padding}{Colors.LINE_COLOR}{Colors.VERTICAL_LEFT}{s_padding} "
                        else:
                            prefix = f"{padding}{Colors.LINE_COLOR}{Colors.VERTICAL}   "

                print(f"{prefix}{Colors.UNHIGHLIGHTED_COLOR}{line_text}{Colors.PRIMARY_TEXT_COLOR}")

    def _wrap_text(text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Se a palavra sozinha é maior que a largura, quebra ela
            if len(word) > max_width:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = ""
                # Quebra a palavra em pedaços
                for i in range(0, len(word), max_width):
                    lines.append(word[i:i+max_width])
            # Se adicionar a palavra ultrapassar a largura
            elif len(current_line) + len(word) + 1 > max_width:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line += word + " "
        
        if current_line.strip():
            lines.append(current_line.strip())
        
        return lines if lines else [""]

    def _box(title, message, box_color=PRIMARY_TEXT_COLOR, text_color=PRIMARY_TEXT_COLOR, width: int = None, center: bool = False):
        left_margin = Colors.MARGIN_LEFT
        message = str(message)
        title = str(title)

        total_width = shutil.get_terminal_size().columns
        if TERMINAL_SIZE < total_width and TERMINAL_SIZE > 0:
            total_width = TERMINAL_SIZE
        
        if center and width:
            max_width = width
        elif width:
            max_width = width - 2 - 2 - left_margin
        else:
            max_width = total_width - 2 - 2 - left_margin*2
        # Processa o texto: divide por \n e depois quebra cada linha
        all_lines = []
        for line in message.split('\n'):
            all_lines.extend(Colors._wrap_text(line, max_width))
        
        # Margem esquerda
        left_space = ' ' * left_margin
        
        # Linha superior (topo)
        top_table = Colors.HORIZONTAL * (max_width + 2)
        top_table = Colors.HORIZONTAL + f" {title} " + top_table[len(title) + 3:]

        if center:
            top_line = f"{box_color}{Colors.TOP_LEFT}{top_table}{Colors.TOP_RIGHT}".center(total_width + len(box_color))
        else:
            top_line = f"{left_space}{box_color}{Colors.TOP_LEFT}{top_table}{Colors.TOP_RIGHT}"
        print(top_line, end="\n")
        
        # Linhas de conteúdo
        for line in all_lines:
            padding = ' ' * (max_width - len(line))
            if center:
                content_line = f"{box_color}{Colors.VERTICAL} {text_color}{line}{padding} {box_color}{Colors.VERTICAL}".center(total_width + len(box_color)*2 + len(text_color))
            else:
                content_line = f"{left_space}{box_color}{Colors.VERTICAL} {text_color}{line}{padding} {box_color}{Colors.VERTICAL}{text_color}"
            print(content_line, end="\n")
        
        # Linha inferior (base)
        if center:
            bottom_line = f"{box_color}{Colors.BOTTOM_LEFT}{Colors.HORIZONTAL * (max_width + 2)}{Colors.BOTTOM_RIGHT}".center(total_width + len(box_color))
        else:
            bottom_line = f"{left_space}{box_color}{Colors.BOTTOM_LEFT}{Colors.HORIZONTAL * (max_width + 2)}{Colors.BOTTOM_RIGHT}{text_color}"
        print(bottom_line, end=f"{text_color}\n")


class Config:
    """Gerenciamento de configurações"""

    def __init__(self):
        self.app_name = "VideoDownloader"
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.channels_file = self.config_dir / "channels.yaml"
        self.log_file = self.config_dir / "downloader.log"
        self.keychain_file = self.config_dir / "keychain.txt"

        self._ensure_dirs()
        self._setup_logging()
        self.settings = self._load_config()

    def _get_config_dir(self) -> Path:
        """Retorna o diretório de configuração conforme o SO"""
        if SYSTEM == "Windows":
            base = Path(os.getenv("LOCALAPPDATA"))
        elif SYSTEM == "Darwin":  # macOS
            base = Path.home() / "Library" / "Application Support"
        else:  # Linux
            base = Path.home() / ".config"

        return base / self.app_name

    def _ensure_dirs(self):
        """Cria diretórios necessários"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """Configura logging"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="[%(asctime)s][%(levelname)s] %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
        )

    def _load_config(self) -> Dict:
        """Carrega configurações"""
        default_config = {
            "download_path": str(Path.home() / "Downloads"),
            "output_format": "ts",
            "show_command": True,
            "auto_decrypt": True,
            "delete_temp": True,
            "api_url": "https://ssd.rdmbr.net/sub/getkeys",
        }

        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                default_config.update(loaded)
        else:
            self.save_config(default_config)

        return default_config

    def save_config(self, config: Dict):
        """Salva configurações"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        self.settings = config

    def load_channels(self) -> List[Dict]:
        """Carrega lista de canais do YAML"""
        script_dir = Path(__file__).parent
        local_channels_file = script_dir / "channels.yaml"

        if local_channels_file.exists():
            with open(local_channels_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("channels", [])

        if self.channels_file.exists():
            with open(self.channels_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("channels", [])

        # Lista padrão de canais
        default_channels = {
            "channels": [
                {"id": 0, "name": "adultswim"},
                {"id": 1, "name": "cartoon"},
                {"id": 2, "name": "nickelodeon"},
                {"id": 3, "name": "mtv"},
                {"id": 4, "name": "sbtrio"},
                {"id": 5, "name": "globorj"},
                {"id": 6, "name": "recordrede"},
                {"id": 7, "name": "recordinteriorsp"},
                {"id": 8, "name": "redetv"},
                {"id": 9, "name": "bandrio"},
                {"id": 10, "name": "bandrs"},
                {"id": 11, "name": "espn"},
                {"id": 12, "name": "espn2"},
                {"id": 13, "name": "espn3"},
                {"id": 14, "name": "espn4"},
                {"id": 15, "name": "espn5"},
                {"id": 16, "name": "espn6"},
                {"id": 17, "name": "xsports"},
                {"id": 18, "name": "getv"},
                {"id": 19, "name": "canaluol"},
                {"id": 20, "name": "combate"},
                {"id": 21, "name": "pfc1"},
                {"id": 22, "name": "pfc2"},
                {"id": 23, "name": "pfc3"},
                {"id": 24, "name": "pfc4"},
                {"id": 25, "name": "pfc5"},
                {"id": 26, "name": "pfc6"},
                {"id": 27, "name": "pfc7"},
                {"id": 28, "name": "pfc8"},
                {"id": 29, "name": "pfc9"},
                {"id": 30, "name": "bandsports"},
                {"id": 31, "name": "bandnews"},
                {"id": 32, "name": "cnnbrasil"},
                {"id": 33, "name": "tnt"},
                {"id": 34, "name": "tntseries"},
                {"id": 35, "name": "tntnovelas"},
                {"id": 36, "name": "space"},
                {"id": 37, "name": "sportv3"},
                {"id": 38, "name": "sportv2"},
                {"id": 39, "name": "sportv"},
                {"id": 40, "name": "globonews"},
                {"id": 41, "name": "gnt"},
                {"id": 42, "name": "multishow"},
                {"id": 43, "name": "viva"},
                {"id": 44, "name": "modoviagem"},
                {"id": 45, "name": "gloob"},
                {"id": 46, "name": "bis"},
            ]
        }

        with open(self.channels_file, "w", encoding="utf-8") as f:
            yaml.dump(default_channels, f, allow_unicode=True, sort_keys=False)

        return default_channels["channels"]


class Logger:
    """Logger com barra de progresso e estatísticas detalhadas"""

    def __init__(self):
        self.start_time = None
        # Adicione isto se quiser manter estatísticas:
        self.stats = {"errors": 0, "warnings": 0}

    def increment_stat(self, stat_name: str, value: int = 1):
        """Incrementa estatística específica"""
        if stat_name in self.stats:
            self.stats[stat_name] += value

    def log_exception(self, exception: Exception, context: str = ""):
        """
        Registra exceção com traceback e trecho de código

        Args:
            exception: Exceção capturada
            context: Contexto adicional
        """
        self.increment_stat("errors")

        # Extrai informações do traceback
        tb_list = traceback.extract_tb(exception.__traceback__)
        if not tb_list:
            print(f"[ERRO] {context} - {str(exception)}")
            return

        last_frame = tb_list[-1]
        file_path = last_frame.filename
        file_name = Path(file_path).name
        line_num = last_frame.lineno
        func_name = last_frame.name

        # Mensagem resumida para console
        short_msg = f"{file_name}:{line_num} em {func_name}() - {type(exception).__name__}: {str(exception)}"
        if context:
            short_msg = f"{context} - {short_msg}"

        # Imprime erro (removido progress_bar.write)
        print(f"\n❌ {short_msg}{Colors.RESET}\n")

        # Extrai código-fonte ao redor do erro
        code_context = self._get_code_context(file_path, line_num, context_lines=3)

        # Exibe código no console
        print(code_context)
        sys.exit(1)

    def _get_code_context(
        self, file_path: str, line_num: int, context_lines: int = 3
    ) -> str:
        """
        Extrai trecho de código ao redor da linha do erro

        Args:
            file_path: Caminho do arquivo
            line_num: Número da linha com erro
            context_lines: Quantas linhas antes/depois mostrar

        Returns:
            String formatada com código
        """
        # Obtém a largura atual do terminal
        cols = shutil.get_terminal_size().columns

        try:
            lines = []
            lines.append(
                f"{Colors.BG_COLOR}{Colors.PRIMARY_TEXT_COLOR}┌"
                + "── Code "
                + ("─" * (cols - 2 - 8))
                + "┐"
            )
            start = max(1, line_num - context_lines)
            end = line_num + context_lines + 1

            for i in range(start, end):
                line = linecache.getline(file_path, i)
                if line:
                    # Marca a linha do erro com indicador
                    if i == line_num:
                        marker = f"│{Colors.SECONDARY_TEXT_COLOR} >>> "
                        new_line = (
                            f"{marker}{i:4d} | {line.rstrip()}"
                            + Colors.PRIMARY_TEXT_COLOR
                            + Colors.BG_COLOR
                        )
                        spaces = max(
                            cols
                            + len(Colors.SECONDARY_TEXT_COLOR)
                            + len(Colors.PRIMARY_TEXT_COLOR)
                            + len(Colors.BG_COLOR)
                            - len(new_line)
                            - 1,
                            0,
                        )
                    else:
                        marker = "│     "
                        new_line = f"{Colors.UNHIGHLIGHT_TEXT_COLOR}{marker}{i:4d} | {line.rstrip()}"
                        spaces = max(
                            cols
                            - len(new_line)
                            + len(Colors.UNHIGHLIGHT_TEXT_COLOR)
                            - 1,
                            0,
                        )

                    lines.append(new_line + (" " * spaces + "│"))

            # Limpa cache do linecache
            linecache.checkcache(file_path)

            lines.append("└" + ("─" * (cols - 2)) + "┘")

            return "\n".join(lines) if lines else "Código fonte não disponível"

        except Exception:
            return "Erro ao ler código fonte"


class KeyboardHandler:
    """Gerencia entrada do teclado para navegação"""

    @staticmethod
    def get_key():
        """Captura tecla pressionada - aguarda input sem polling"""
        if SYSTEM == "Windows":
            key = msvcrt.getch()
            if key == b"\xe0" or key == b"\x00":  # Tecla especial
                key = msvcrt.getch()
                if key == b"H":  # Seta para cima
                    return "up"
                elif key == b"P":  # Seta para baixo
                    return "down"
                elif key == b"K":  # Seta para esquerda
                    return "left"
                elif key == b"M":  # Seta para direita
                    return "right"
            elif key == b"\r":  # Enter
                return "enter"
            elif key == b"\x1b":  # ESC
                return "esc"
            else:
                try:
                    return key.decode("utf-8", errors="ignore")
                except:
                    return None
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == "\x1b":  # Sequência de escape
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        ch3 = sys.stdin.read(1)
                        if ch3 == "A":
                            return "up"
                        elif ch3 == "B":
                            return "down"
                        elif ch3 == "C":
                            return "right"
                        elif ch3 == "D":
                            return "left"
                    return "esc"
                elif ch == "\r" or ch == "\n":
                    return "enter"
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None


class Credentials:
    """Gerenciamento de credenciais"""

    SERVICE_NAME = "VideoDownloader"

    @staticmethod
    def save_credentials(username: str, password: str):
        """Salva credenciais no keyring"""
        keyring.set_password(Credentials.SERVICE_NAME, username, password)
        logging.info(f"Credenciais salvas para o usuário {username}")

    @staticmethod
    def get_credentials() -> Optional[Tuple[str, str]]:
        """Recupera credenciais"""
        try:
            # Tenta recuperar do keyring
            usernames = keyring.get_credential(Credentials.SERVICE_NAME, None)
            if usernames:
                username = usernames.username
                password = keyring.get_password(Credentials.SERVICE_NAME, username)
                return username, password
        except:
            pass
        return None

    @staticmethod
    def delete_credentials():
        """Remove credenciais"""
        try:
            creds = Credentials.get_credentials()
            if creds:
                keyring.delete_password(Credentials.SERVICE_NAME, creds[0])
                logging.info("Credenciais removidas")
        except:
            pass


class Downloader:
    """Classe principal para download"""

    def __init__(self, config: Config):
        self.config = config

    def get_api_data(
        self, channel: str, start: str = None, end: str = None, mode: str = "live"
    ) -> Tuple[str, str]:
        """Faz requisição à API para obter URL e chave"""

        creds = Credentials.get_credentials()
        if not creds:
            Colors.center_title("Credenciais")
            Colors.warning("Credenciais não encontradas!")
            username = input(f"{Colors.select_item("Usuário")}")
            import getpass

            password = getpass.getpass(f"{Colors.PRIMARY_TEXT_COLOR}    Senha: ")
            Credentials.save_credentials(username, password)
            creds = (username, password)

        auth_string = f"{creds[0]}:{creds[1]}"
        auth_b64 = base64.b64encode(auth_string.encode()).decode()

        # Monta parâmetros
        if mode == "dvr" and start and end:
            params = f"?&start={start}&end={end}"
        else:
            params = "?direct=1"

        pattern = r"^[a-z]{2}-[a-z0-9]+$"
        if not re.match(pattern, channel):
            channel = f"vp-{channel}"

        headers = {
            "Authorization": f"Basic {auth_b64}",
            "X-Channel": channel,
            "X-Original-URI": params,
        }

        try:
            response = requests.get(
                self.config.settings["api_url"], headers=headers, timeout=10
            )

            if response.status_code == 200:
                url = (
                    response.headers.get("X-URL", "")
                    .replace('"', "")
                    .replace("data.rdmbr.net/p/https/", "")
                )
                key = response.headers.get("X-Key", "").replace('"', "")

                if "index.mpd/Manifest.mpd" in url:
                    url = url.replace("index.mpd/Manifest.mpd", "index.mpd/Manifest")

                # Imprime chave e URL
                Colors.center_title("Dados da API")

                # Separa múltiplas chaves se houver
                Colors.item("Chave",color=Colors.HIGHLIGHTED_COLOR)
                Colors.list_item([key])
                keys = key.split(",")

                Colors.item("URL",color=Colors.HIGHLIGHTED_COLOR)
                Colors.list_item([url])

                # Salva no keychain
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                with open(self.config.keychain_file, "a", encoding="utf-8") as f:
                    for k in keys:
                        f.write(f"[{timestamp}] vp-{channel} | {k.strip()}\n")

                logging.info(f"API retornou URL e chave para {channel}")
                return url, key
            else:
                raise Exception(f"Erro na API: {response.status_code}")

        except Exception as e:
            Colors.error("Erro ao acessar API", e)
            logging.error(f"Erro na API: {e}")
            return None, None

    def download_video(
        self,
        url: str,
        key: str,
        channel: str,
        output_format: str = "ts",
        start_time: str = None,
    ):
        """Realiza o download usando N_m3u8DL-RE"""

        # Verifica se N_m3u8DL-RE está disponível
        nm3u8dl = self._find_executable("N_m3u8DL-RE")
        if not nm3u8dl:
            Colors.error("N_m3u8DL-RE não encontrado!")
            return False

        mp4decrypt = self._find_executable("mp4decrypt")
        if not mp4decrypt:
            Colors.error("mp4decrypt não encontrado!")
            return False

        # Prepara nome do arquivo
        if start_time:
            timestamp = start_time[:8] + "_" + start_time[8:] + "00"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{channel}_{timestamp}"
        output_path = Path(self.config.settings["download_path"])

        # Monta comando
        cmd = [
            nm3u8dl,
            f'"{url}"',
            f"-M format={output_format}",
            "--no-log",
            "--log-level ERROR",
            '--header "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 15.7; rv:143.0) Gecko/20100101 Firefox/143.0"',
            "--live-real-time-merge",
            "--live-pipe-mux",
            f"--save-name {filename}",
            f'--save-dir "{output_path}"',
            f'--tmp-dir "{output_path}"',
            "--concurrent-download"
        ]

        if key:
            joined_keys = " --key ".join([key])
            cmd.append(f"--key {joined_keys}")

        if self.config.settings.get("delete_temp", True):
            cmd.append("--del-after-done")

        if self.config.settings.get("show_command", True):
            Colors.item("Comando",color=Colors.HIGHLIGHTED_COLOR)
            Colors.list_item([(' '.join(cmd))])

        # Executa download com saída nativa
        Colors.center_title("Download")
        Colors.item(f"Iniciando download de {channel}...\n")
        logging.info(f"Comando: {' '.join(cmd)}")

        try:
            # Executa sem capturar saída para permitir interatividade
            process = subprocess.run(" ".join(cmd), shell=True)

            if process.returncode == 0:
                print(Colors.BG_COLOR)
                Colors.ok("✓ Download concluído!")
                Colors.info(f"{output_path / filename}"+f".{output_format}", "Salvo em")
                logging.info(f"Download concluído: {filename}")
                return True
            else:
                print(Colors.BG_COLOR)
                Colors.error(f"Erro no download {process.returncode}")
                return False

        except Exception as e:
            Colors.error("Erro ao executar download", e)
            logging.error(f"Erro no download: {e}")
            return False

    def _find_executable(self, name: str) -> Optional[str]:
        """Procura executável no sistema"""
        if SYSTEM == "Windows":
            name = f"{name}.exe"

        # Verifica no PATH
        from shutil import which

        exe = which(name)
        if exe:
            return exe

        # Verifica no diretório do script
        script_dir = Path(__file__).parent
        local_exe = script_dir / name
        if local_exe.exists():
            return str(local_exe)

        return None


def show_channel_menu(config: Config) -> Optional[str]:
    """Mostra menu de seleção de canais com navegação por teclado"""
    channels = config.load_channels()
    selected = 0
    kb = KeyboardHandler()

    def draw_menu(key = ""):
        Colors.clear_screen()

        # Título centralizado
        title = TITULO
        
        top_table = f"╭{'─' * 25}┬{'─' * 25}┬{'─' * 25}╮"
        table_width = TERMINAL_SIZE - len(top_table)
        table_padding = " " * (math.floor(table_width / 2))

        top_table = "╭─── " + title + " " + top_table[len(title) + 6 :]

        # Tabela com 3 colunas
        second_top_table = f"│{' ' * 25}│{' ' * 25}│{' ' * 25}│"

        second_top_table = (
            "│    " + " " * len(title) + " " + second_top_table[len(title) + 6 :]
        )
        Colors.item()
        print(f"{Colors.PRIMARY_TEXT_COLOR}{table_padding}{top_table}{table_padding}")
        print(
            f"{Colors.PRIMARY_TEXT_COLOR}{table_padding}{second_top_table}{table_padding}"
        )

        for i in range(0, len(channels), 3):
            parts = []
            for j in range(3):
                idx = i + j
                if idx < len(channels):
                    ch = channels[idx]
                    prefix = "▶" if idx == selected else " "

                    if idx == selected:
                        text = f"{Colors.HIGHLIGHTED_COLOR}{prefix} {ch['id']:2d}. {ch['name']:<19}"
                    else:
                        text = f"{Colors.PRIMARY_TEXT_COLOR}{prefix} {ch['id']:2d}. {ch['name']:<19}"
                    parts.append(text)
                else:
                    parts.append(" " * 25)

            print(
                f"{Colors.PRIMARY_TEXT_COLOR}{table_padding}│{parts[0]}{Colors.PRIMARY_TEXT_COLOR}│",
                end=f"",
            )
            if len(parts) > 1:
                print(f"{parts[1]}{Colors.PRIMARY_TEXT_COLOR}│", end="")
            if len(parts) > 2:
                print(f"{parts[2]}{Colors.PRIMARY_TEXT_COLOR}│{table_padding}")
            else:
                print()

        bottom_table = f"{Colors.PRIMARY_TEXT_COLOR}╰{'─' * 25}┴{'─' * 25}┴{'─' * 25}╯"
        print(
            f"{Colors.PRIMARY_TEXT_COLOR}{table_padding}{bottom_table}{table_padding}"
        )

        # Opções
        Colors.center_text(f"v{VERSION}     @limaalef", color=Colors.UNHIGHLIGHTED_COLOR, highlight=VERSION)
        Colors.center_text(
            "90 = Inserir nome do canal  |  98 = Inserir URL  |  99 = Configurações",
            Colors.SECONDARY_TEXT_COLOR,
        )
        Colors.center_text(
            f"Insira o número da opção ou use as setas ↑↓←→ para navegar e Enter para selecionar",
            Colors.UNHIGHLIGHTED_COLOR,
        )
        Colors.item()

    draw_menu()
    number_buffer = ""
    key = ""

    while True:
        key = kb.get_key()
        
        if key == "up":
            if selected >= 3:
                selected -= 3
                draw_menu()
        elif key == "down":
            if selected + 3 < len(channels):
                selected += 3
                draw_menu()
        elif key == "left":
            if selected > 0:
                selected -= 1
                draw_menu()
        elif key == "right":
            if selected < len(channels) - 1:
                selected += 1
                draw_menu()
        elif key == "enter":
            return channels[selected]["name"]
        elif key == "esc":
            return None
        elif key and key.isdigit():
            number_buffer += key
            print(f"\r    Opção escolhida: {Colors.HIGHLIGHTED_COLOR}{number_buffer}{Colors.PRIMARY_TEXT_COLOR}", end="")

            if len(number_buffer) == 2:
                if number_buffer == "90":
                    Colors.item()
                    name = input(f"{Colors.select_item("Nome do canal")}")
                    return name
                elif number_buffer == "98":
                    return "URL_MANUAL"
                elif number_buffer == "99":
                    show_settings_menu(config)
                    number_buffer = ""
                    draw_menu()
                else:
                    try:
                        channel_id = int(number_buffer)
                        for ch in channels:
                            if ch["id"] == channel_id:
                                return ch["name"]
                    except:
                        pass
                    number_buffer = ""
        else:
            number_buffer = ""


def select_datetime(prompt: str, default_now: bool = True) -> str:
    """Seletor interativo de data e hora com navegação por teclado"""
    kb = KeyboardHandler()

    now = datetime.now()
    min_date = now - timedelta(days=8)
    selected_date = now if default_now else now

    fields = [
        selected_date.day,
        selected_date.month,
        selected_date.year,
        selected_date.hour,
        selected_date.minute,
    ]

    current_field = 0

    def format_datetime_line():
        parts = []
        for i, value in enumerate(fields):
            if i == current_field:
                if i == 2:
                    parts.append(
                        f"{Colors.SELECTED_BG}{Colors.PRIMARY_TEXT_COLOR}{value:04d}{Colors.BG_COLOR}"
                    )
                elif i == 3 or i == 4:
                    parts.append(
                        f"{Colors.SELECTED_BG}{Colors.PRIMARY_TEXT_COLOR}{value:02d}{Colors.BG_COLOR}"
                    )
                else:
                    parts.append(
                        f"{Colors.SELECTED_BG}{Colors.PRIMARY_TEXT_COLOR}{value:02d}{Colors.BG_COLOR}"
                    )
            else:
                if i == 2:
                    parts.append(f"{Colors.PRIMARY_TEXT_COLOR}{value:04d}")
                elif i == 3 or i == 4:
                    parts.append(f"{Colors.PRIMARY_TEXT_COLOR}{value:02d}")
                else:
                    parts.append(f"{Colors.PRIMARY_TEXT_COLOR}{value:02d}")

        return f"      {parts[0]}/{parts[1]}/{parts[2]} {parts[3]}:{parts[4]} "

    Colors.item(
        f"{Colors.HIGHLIGHTED_COLOR}{prompt}  {Colors.UNHIGHLIGHTED_COLOR}(↑↓←→ Enter/ESC)"
    )
    print(format_datetime_line(), end="", flush=True)

    while True:
        key = kb.get_key()
        needs_update = False
        show_error = None

        if key == "left":
            current_field = max(0, current_field - 1)
            needs_update = True
        elif key == "right":
            current_field = min(4, current_field + 1)
            needs_update = True
        elif key == "up":
            if current_field == 0:
                max_day = 31
                if fields[1] in [4, 6, 9, 11]:
                    max_day = 30
                elif fields[1] == 2:
                    max_day = (
                        29
                        if (
                            fields[2] % 4 == 0
                            and (fields[2] % 100 != 0 or fields[2] % 400 == 0)
                        )
                        else 28
                    )
                fields[0] = fields[0] % max_day + 1
            elif current_field == 1:
                fields[1] = fields[1] % 12 + 1
            elif current_field == 2:
                fields[2] += 1
                if fields[2] > now.year:
                    fields[2] = min_date.year
            elif current_field == 3:
                fields[3] = (fields[3] + 1) % 24
            elif current_field == 4:
                fields[4] = (fields[4] + 1) % 60
            needs_update = True
        elif key == "down":
            if current_field == 0:
                max_day = 31
                if fields[1] in [4, 6, 9, 11]:
                    max_day = 30
                elif fields[1] == 2:
                    max_day = (
                        29
                        if (
                            fields[2] % 4 == 0
                            and (fields[2] % 100 != 0 or fields[2] % 400 == 0)
                        )
                        else 28
                    )
                fields[0] = max_day if fields[0] == 1 else fields[0] - 1
            elif current_field == 1:
                fields[1] = 12 if fields[1] == 1 else fields[1] - 1
            elif current_field == 2:
                fields[2] -= 1
                if fields[2] < min_date.year:
                    fields[2] = now.year
            elif current_field == 3:
                fields[3] = (fields[3] - 1) % 24
            elif current_field == 4:
                fields[4] = (fields[4] - 1) % 60
            needs_update = True
        elif key == "enter":
            try:
                selected = datetime(
                    fields[2], fields[1], fields[0], fields[3], fields[4]
                )
                if selected < min_date:
                    show_error = "Data não pode ser anterior a 7 dias!"
                elif selected > now:
                    show_error = "Data não pode ser no futuro!"
                else:
                    print()
                    return selected.strftime("%Y%m%d%H%M")
            except ValueError:
                show_error = "Data inválida!"
        elif key == "esc":
            print()
            return None

        if needs_update or show_error:
            # Limpa a linha atual
            print("\r" + " " * (Colors.MARGIN_LEFT + 2 + 30) + "\r", end="", flush=True)

            if show_error:
                print(f"{Colors.ERROR_COLOR}    {show_error}", end="", flush=True)
                import time

                time.sleep(2)
                print("\r" + " " * (Colors.MARGIN_LEFT + 2 + 30) + "\r", end="", flush=True)

            print(format_datetime_line(), end="", flush=True)


def show_settings_menu(config: Config):
    """Menu de configurações"""
    Colors.clear_screen()
    Colors.print_banner()
    Colors.center_title("Configurações")

    settings = config.settings

    Colors.item("1. Pasta de download", f"{settings['download_path']}")
    Colors.item("2. Formato de saída", f"{settings['output_format']}")
    Colors.item("3. Mostrar comandos dados aos programas", f"{settings['show_command']}")
    Colors.item("4. Deletar temporários", f"{settings['delete_temp']}")
    Colors.item("5. Gerenciar credenciais")
    Colors.item("0. Voltar")

    choice = input(f"\n{Colors.select_item("Opção", "0")}")

    if choice == "1":
        new_path = (
            input(f"{Colors.select_item("Novo caminho", settings['download_path'])}")
            or settings["download_path"]
        )
        settings["download_path"] = new_path
        config.save_config(settings)
    elif choice == "2":
        fmt = input(f"{Colors.select_item("Formato (mp4/ts)", "ts")}") or "ts"
        if fmt in ["mp4", "ts"]:
            settings["output_format"] = fmt
            config.save_config(settings)
    elif choice == "3":
        settings["show_command"] = not settings["show_command"]
        config.save_config(settings)
    elif choice == "4":
        settings["delete_temp"] = not settings["delete_temp"]
        config.save_config(settings)
    elif choice == "5":
        manage_credentials()


def manage_credentials():
    """Gerencia credenciais"""
    Colors.clear_screen()
    Colors.print_banner()
    Colors.center_title("Gerenciar Credenciais")
    Colors.item("1. Alterar credenciais")
    Colors.item("2. Remover credenciais")
    Colors.item("0. Voltar")

    choice = input(f"\n{Colors.select_item("Opção", "0")}")

    if choice == "1":
        username = input(f"{Colors.select_item("Novo usuário")}")
        import getpass

        password = getpass.getpass(f"{Colors.PRIMARY_TEXT_COLOR}    Nova senha: ")
        Credentials.save_credentials(username, password)
        print(f"{Colors.SUCCESS_COLOR}Credenciais atualizadas!")
    elif choice == "2":
        confirm = input(f"{Colors.select_item("Confirmar remoção? (s/N)")}")
        if confirm.lower() == "s":
            Credentials.delete_credentials()
            print(f"{Colors.WARNING_COLOR}Credenciais removidas")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Video Downloader")
    parser.add_argument("channel", nargs="?", help="Nome do canal ou URL")
    parser.add_argument("--start", help="Data/hora início (YYYYMMDDHHMMSS)")
    parser.add_argument("--end", help="Data/hora fim (YYYYMMDDHHMMSS)")
    parser.add_argument("--format", choices=["mp4", "ts"], default="ts")
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        nargs="+",
        dest="key",
        help="Chave de descriptografia",
    )

    args = parser.parse_args()

    config = Config()
    downloader = Downloader(config)

    # Modo linha de comando
    if args.channel:
        Colors.print_banner()
        if args.channel.startswith("http"):
            url = args.channel
            if "aiv-cdn.net/iad-nitro/jab-assets" in url:
                key = "d59c68c9d5159c6f794491790d1f0419:ae7f422f97c5ae22a538551ba2ff97db" #"6e37fc06a2c4347e9168d3c8616244bd:350bca1ea2e5a335799a886333738839"
            else:
                key = args.key or input(f"{Colors.select_item("Chave de descriptografia")}")
            channel_name = "manual"
        else:
            mode = "dvr" if args.start and args.end else "live"
            url, key = downloader.get_api_data(args.channel, args.start, args.end, mode)
            channel_name = args.channel

        if url:
            fmt = config.settings.get("output_format", "ts")
            downloader.download_video(url, key, channel_name, fmt, args.start)
    else:
        # Modo interativo
        while True:
            channel = show_channel_menu(config)

            if not channel:
                print(
                    f"\n{Colors.INFO_COLOR}    Encerrando...{Colors.PRIMARY_TEXT_COLOR}"
                )
                break

            if channel == "URL_MANUAL":
                url = input(f"\n{Colors.select_item("URL do vídeo")}")
                key = input(f"{Colors.select_item("Chave de descriptografia")}")
                channel_name = "manual"
            else:
                # Pergunta se é live ou DVR
                Colors.center_title("Modo de download")
                Colors.item("Canal selecionado", channel)
                Colors.item()
                Colors.item(f"Ao vivo", index="1")
                Colors.item(f"DVR", index="2")
                Colors.item()
                mode_choice = (input(f"{Colors.select_item("Escolha", "1")}") or "1")

                if mode_choice == "2":
                    Colors.center_title("Seleção de período para DVR")
                    start = select_datetime("Data/hora de início")
                    if not start:
                        continue

                    Colors.item()
                    end = select_datetime("Data/hora de fim", default_now=True)
                    if not end:
                        continue

                    url, key = downloader.get_api_data(channel, start, end, "dvr")
                    channel_name = channel
                else:
                    url, key = downloader.get_api_data(channel, mode="live")
                    channel_name = channel
                    start = None

            if (url and key) or (url and channel == "URL_MANUAL"):
                fmt = config.settings.get("output_format", "mp4")
                downloader.download_video(
                    url, key, channel_name, fmt, start if "start" in locals() else None
                )
            else:
                Colors.error("Não foi possível obter dados da API")

            # Pergunta se quer fazer outro download
            Colors.item()
            again = input(f"{Colors.select_item("Fazer outro download? (S/n)")}")
            if again.lower() == "n":
                break


if __name__ == "__main__":
    main()
