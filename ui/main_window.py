import customtkinter as ctk
import cv2
from PIL import Image

from vision.camera import Camera
from vision.detector import FaceDetector
from vision.embedder import FaceEmbedder
from vision.recognizer import FaceRecognizer

from database.database import Database
from ui.register_window import RegisterWindow


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================================================
        # APARÊNCIA
        # =========================================================

        ctk.set_appearance_mode("light")

        self.title("Sistema de Controle de Acesso - IFF")
        self.geometry("1200x720")
        self.minsize(1000, 650)

        # Cores
        self.COLOR_GREEN = "#2F9E41"
        self.COLOR_DARK_GREEN = "#1F7A32"
        self.COLOR_RED = "#C62828"
        self.COLOR_ORANGE = "#D97706"
        self.COLOR_DARK = "#1F2937"
        self.COLOR_GRAY = "#6B7280"
        self.COLOR_LIGHT_GRAY = "#F3F4F6"
        self.COLOR_BORDER = "#E5E7EB"
        self.COLOR_WHITE = "#FFFFFF"

        # =========================================================
        # COMPONENTES
        # =========================================================

        self.camera = Camera()
        self.detector = FaceDetector()
        self.embedder = FaceEmbedder()

        self.database = Database()

        self.recognizer = FaceRecognizer(
            self.database
        )

        # =========================================================
        # CONTROLE
        # =========================================================

        self.current_frame = None

        self.frame_counter = 0
        self.recognition_interval = 10

        # =========================================================
        # EVENTOS
        # =========================================================

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # F11 = fullscreen
        self.bind(
            "<F11>",
            self.toggle_fullscreen
        )

        # ESC = sair do fullscreen
        self.bind(
            "<Escape>",
            self.exit_fullscreen
        )

        # =========================================================
        # INTERFACE
        # =========================================================

        self.create_widgets()

        # Estado inicial
        self.set_waiting_state()

        # Câmera
        self.update_camera()

    # =============================================================
    # INTERFACE
    # =============================================================

    def create_widgets(self):

        # Fundo principal
        self.configure(
            fg_color=self.COLOR_LIGHT_GRAY
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # =========================================================
        # HEADER
        # =========================================================

        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_WHITE,
            corner_radius=0,
            height=120
        )

        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Coluna da esquerda cresce
        self.header_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # =========================================================
        # ÁREA DA MARCA
        # =========================================================

        self.brand_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )

        self.brand_frame.grid(
            row=0,
            column=0,
            padx=(30, 20),
            pady=15,
            sticky="w"
        )

        # ---------------------------------------------------------
        # LOGO
        # ---------------------------------------------------------

        try:

            logo_image = Image.open(
                "assets/iff_logo.png"
            )

            self.logo_image = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(220, 60)
            )

            self.logo_label = ctk.CTkLabel(
                self.brand_frame,
                image=self.logo_image,
                text=""
            )

            self.logo_label.pack(
                anchor="w"
            )

        except Exception as error:

            print(
                "Não foi possível carregar a logo:",
                error
            )

            self.logo_label = ctk.CTkLabel(
                self.brand_frame,
                text="Instituto Federal Fluminense",
                font=("Arial", 22, "bold"),
                text_color=self.COLOR_DARK
            )

            self.logo_label.pack(
                anchor="w"
            )

        # ---------------------------------------------------------
        # NOME DO SISTEMA
        # ---------------------------------------------------------

        self.system_label = ctk.CTkLabel(
            self.brand_frame,
            text="Sistema de Controle de Acesso",
            font=("Arial", 15),
            text_color=self.COLOR_GRAY
        )

        self.system_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        # =========================================================
        # CONTEÚDO PRINCIPAL
        # =========================================================

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content_frame.grid(
            row=1,
            column=0,
            padx=30,
            pady=25,
            sticky="nsew"
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=3
        )

        self.content_frame.grid_columnconfigure(
            1,
            weight=2
        )

        self.content_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # =========================================================
        # CARD DA CÂMERA
        # =========================================================

        self.camera_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.COLOR_WHITE,
            corner_radius=15
        )

        self.camera_card.grid(
            row=0,
            column=0,
            padx=(0, 15),
            sticky="nsew"
        )

        # ---------------------------------------------------------
        # TÍTULO DA CÂMERA
        # ---------------------------------------------------------

        self.camera_title = ctk.CTkLabel(
            self.camera_card,
            text="IDENTIFICAÇÃO FACIAL",
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_GRAY
        )

        self.camera_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        # ---------------------------------------------------------
        # VÍDEO
        # ---------------------------------------------------------

        self.camera_label = ctk.CTkLabel(
            self.camera_card,
            text="",
            fg_color="#111827",
            corner_radius=10
        )

        self.camera_label.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=(0, 20)
        )

        # =========================================================
        # CARD DE IDENTIFICAÇÃO
        # =========================================================

        self.info_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.COLOR_WHITE,
            corner_radius=15
        )

        self.info_card.grid(
            row=0,
            column=1,
            padx=(15, 0),
            sticky="nsew"
        )

        # ---------------------------------------------------------
        # TÍTULO
        # ---------------------------------------------------------

        self.info_title = ctk.CTkLabel(
            self.info_card,
            text="IDENTIFICAÇÃO",
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_GRAY
        )

        self.info_title.pack(
            anchor="w",
            padx=30,
            pady=(25, 0)
        )

        # ---------------------------------------------------------
        # ÍCONE / INDICADOR
        # ---------------------------------------------------------

        self.status_icon = ctk.CTkLabel(
            self.info_card,
            text="◎",
            font=("Arial", 55, "bold"),
            text_color=self.COLOR_GRAY
        )

        self.status_icon.pack(
            pady=(50, 5)
        )

        # ---------------------------------------------------------
        # STATUS
        # ---------------------------------------------------------

        self.status_label = ctk.CTkLabel(
            self.info_card,
            text="AGUARDANDO IDENTIFICAÇÃO",
            font=("Arial", 20, "bold"),
            text_color=self.COLOR_DARK
        )

        self.status_label.pack(
            pady=(5, 5)
        )

        # ---------------------------------------------------------
        # TEXTO AUXILIAR
        # ---------------------------------------------------------

        self.message_label = ctk.CTkLabel(
            self.info_card,
            text="Posicione-se diante da câmera",
            font=("Arial", 14),
            text_color=self.COLOR_GRAY
        )

        self.message_label.pack(
            pady=(0, 25)
        )

        # ---------------------------------------------------------
        # NOME
        # ---------------------------------------------------------

        self.name_label = ctk.CTkLabel(
            self.info_card,
            text="",
            font=("Arial", 24, "bold"),
            text_color=self.COLOR_DARK
        )

        self.name_label.pack(
            pady=(15, 5)
        )

        # ---------------------------------------------------------
        # MATRÍCULA
        # ---------------------------------------------------------

        self.registration_label = ctk.CTkLabel(
            self.info_card,
            text="",
            font=("Arial", 16),
            text_color=self.COLOR_GRAY
        )

        self.registration_label.pack()

        # ---------------------------------------------------------
        # BOTÃO CADASTRO
        # ---------------------------------------------------------

        self.register_button = ctk.CTkButton(
            self.info_card,
            text="+  CADASTRAR PESSOA",
            height=48,
            font=("Arial", 14, "bold"),
            fg_color=self.COLOR_GREEN,
            hover_color=self.COLOR_DARK_GREEN,
            command=self.open_registration
        )

        self.register_button.pack(
            side="bottom",
            padx=30,
            pady=30,
            fill="x"
        )

        # =========================================================
        # RODAPÉ
        # =========================================================

        self.footer_frame = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_WHITE,
            corner_radius=0,
            height=45
        )

        self.footer_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text=(
                "Protótipo de reconhecimento facial "
                "para controle de acesso"
            ),
            font=("Arial", 12),
            text_color=self.COLOR_GRAY
        )

        self.footer_label.pack(
            pady=12
        )

    # =============================================================
    # ESTADOS DA INTERFACE
    # =============================================================

    def set_waiting_state(self):

        self.status_icon.configure(
            text="◎",
            text_color=self.COLOR_GRAY
        )

        self.status_label.configure(
            text="AGUARDANDO IDENTIFICAÇÃO",
            text_color=self.COLOR_DARK
        )

        self.message_label.configure(
            text="Posicione-se diante da câmera"
        )

        self.name_label.configure(
            text=""
        )

        self.registration_label.configure(
            text=""
        )

    def set_authorized_state(self, user):

        self.status_icon.configure(
            text="✓",
            text_color=self.COLOR_GREEN
        )

        self.status_label.configure(
            text="ACESSO AUTORIZADO",
            text_color=self.COLOR_GREEN
        )

        self.message_label.configure(
            text="Identidade verificada"
        )

        self.name_label.configure(
            text=user["name"]
        )

        self.registration_label.configure(
            text=(
                "Matrícula: "
                f"{user['registration_number']}"
            )
        )

    def set_unknown_state(self):

        self.status_icon.configure(
            text="✕",
            text_color=self.COLOR_RED
        )

        self.status_label.configure(
            text="NÃO IDENTIFICADO",
            text_color=self.COLOR_RED
        )

        self.message_label.configure(
            text="Usuário não encontrado"
        )

        self.name_label.configure(
            text=""
        )

        self.registration_label.configure(
            text=""
        )

    def set_multiple_faces_state(self):

        self.status_icon.configure(
            text="!",
            text_color=self.COLOR_ORANGE
        )

        self.status_label.configure(
            text="MÚLTIPLOS ROSTOS",
            text_color=self.COLOR_ORANGE
        )

        self.message_label.configure(
            text="Mantenha apenas uma pessoa diante da câmera"
        )

        self.name_label.configure(
            text=""
        )

        self.registration_label.configure(
            text=""
        )

    # =============================================================
    # CÂMERA / RECONHECIMENTO
    # =============================================================

    def update_camera(self):

        frame = self.camera.read()

        if frame is not None:

            # -----------------------------------------------------
            # FRAME ORIGINAL
            # -----------------------------------------------------

            self.current_frame = frame.copy()

            # -----------------------------------------------------
            # DETECÇÃO
            # -----------------------------------------------------

            faces = self.detector.detect(
                frame
            )

            # -----------------------------------------------------
            # ESTADO: NENHUM ROSTO
            # -----------------------------------------------------

            if len(faces) == 0:

                self.set_waiting_state()

            # -----------------------------------------------------
            # ESTADO: MAIS DE UM ROSTO
            # -----------------------------------------------------

            elif len(faces) > 1:

                self.set_multiple_faces_state()

            # -----------------------------------------------------
            # ESTADO: UM ROSTO
            # -----------------------------------------------------

            elif len(faces) == 1:

                self.frame_counter += 1

                if (
                    self.frame_counter
                    >= self.recognition_interval
                ):

                    self.frame_counter = 0

                    face = faces[0]

                    cropped_face = (
                        self.detector.crop_face(
                            frame,
                            face
                        )
                    )

                    if cropped_face.size > 0:

                        # -----------------------------------------
                        # EMBEDDING
                        # -----------------------------------------

                        embedding = (
                            self.embedder.generate(
                                cropped_face
                            )
                        )

                        # -----------------------------------------
                        # RECONHECIMENTO
                        # -----------------------------------------

                        user, similarity = (
                            self.recognizer.recognize(
                                embedding
                            )
                        )

                        if user:

                            self.set_authorized_state(
                                user
                            )

                        else:

                            self.set_unknown_state()

            # =====================================================
            # FRAME PARA EXIBIÇÃO
            # =====================================================

            # Espelha somente visualmente
            display_frame = cv2.flip(
                frame,
                1
            )

            frame_width = (
                display_frame.shape[1]
            )

            # -----------------------------------------------------
            # BOUNDING BOX
            # -----------------------------------------------------

            for face in faces:

                x, y, w, h = face["bbox"]

                # Corrige posição X porque
                # a imagem está espelhada
                x_mirrored = (
                    frame_width
                    - x
                    - w
                )

                cv2.rectangle(
                    display_frame,
                    (x_mirrored, y),
                    (
                        x_mirrored + w,
                        y + h
                    ),
                    (0, 255, 0),
                    2
                )

            # -----------------------------------------------------
            # BGR -> RGB
            # -----------------------------------------------------

            display_frame = cv2.cvtColor(
                display_frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(
                display_frame
            )

            # -----------------------------------------------------
            # MOSTRA NA INTERFACE
            # -----------------------------------------------------

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(640, 480)
            )

            self.camera_label.configure(
                image=ctk_image
            )

            self.camera_label.image = (
                ctk_image
            )

        # Próximo frame
        self.after(
            30,
            self.update_camera
        )

    # =============================================================
    # CADASTRO
    # =============================================================

    def open_registration(self):

        RegisterWindow(
            parent=self,
            detector=self.detector,
            embedder=self.embedder,
            database=self.database
        )

    # =============================================================
    # FULLSCREEN
    # =============================================================

    def toggle_fullscreen(self, event=None):

        current_state = self.attributes(
            "-fullscreen"
        )

        self.attributes(
            "-fullscreen",
            not current_state
        )

    def exit_fullscreen(self, event=None):

        self.attributes(
            "-fullscreen",
            False
        )

    # =============================================================
    # FECHAR
    # =============================================================

    def close(self):

        self.camera.release()

        self.detector.close()

        self.destroy()