import customtkinter as ctk
import cv2
from PIL import Image
from tkinter import messagebox


class RegisterWindow(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        detector,
        embedder,
        database
    ):
        super().__init__(parent)

        # =========================================================
        # REFERÊNCIAS
        # =========================================================

        self.parent = parent
        self.detector = detector
        self.embedder = embedder
        self.database = database

        # Frame ORIGINAL usado para gerar o embedding
        self.current_frame = None

        # =========================================================
        # CORES
        # =========================================================

        self.COLOR_GREEN = "#2F9E41"
        self.COLOR_DARK_GREEN = "#1F7A32"
        self.COLOR_RED = "#C62828"
        self.COLOR_DARK = "#1F2937"
        self.COLOR_GRAY = "#6B7280"
        self.COLOR_LIGHT_GRAY = "#F3F4F6"
        self.COLOR_WHITE = "#FFFFFF"

        # =========================================================
        # JANELA
        # =========================================================

        self.title(
            "Cadastrar Pessoa - IFF"
        )

        self.geometry(
            "950x650"
        )

        self.minsize(
            850,
            600
        )

        self.configure(
            fg_color=self.COLOR_LIGHT_GRAY
        )

        # Associa à janela principal
        self.transient(parent)

        # Impede interação com a principal
        # enquanto o cadastro estiver aberto
        self.grab_set()

        # =========================================================
        # INTERFACE
        # =========================================================

        self.create_widgets()

        # =========================================================
        # CÂMERA
        # =========================================================

        self.update_camera()

    # =============================================================
    # INTERFACE
    # =============================================================

    def create_widgets(self):

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
            text="Cadastro de Usuário • Sistema de Controle de Acesso",
            font=("Arial", 15),
            text_color=self.COLOR_GRAY
        )

        self.system_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        
        # =========================================================
        # CONTEÚDO
        # =========================================================

        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content_frame.grid(
            row=1,
            column=0,
            padx=25,
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
            padx=(0, 12),
            sticky="nsew"
        )

        # ---------------------------------------------------------
        # TÍTULO DA CÂMERA
        # ---------------------------------------------------------

        self.camera_title = ctk.CTkLabel(
            self.camera_card,
            text="CAPTURA FACIAL",
            font=("Arial", 13, "bold"),
            text_color=self.COLOR_GRAY
        )

        self.camera_title.pack(
            anchor="w",
            padx=20,
            pady=(18, 10)
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
            padx=18,
            pady=(0, 12)
        )

        # ---------------------------------------------------------
        # STATUS DO ROSTO
        # ---------------------------------------------------------

        self.status_label = ctk.CTkLabel(
            self.camera_card,
            text="Posicione o rosto diante da câmera",
            font=("Arial", 14),
            text_color=self.COLOR_GRAY
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # =========================================================
        # CARD DE DADOS
        # =========================================================

        self.form_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.COLOR_WHITE,
            corner_radius=15
        )

        self.form_card.grid(
            row=0,
            column=1,
            padx=(12, 0),
            sticky="nsew"
        )

        # ---------------------------------------------------------
        # TÍTULO
        # ---------------------------------------------------------

        self.form_title = ctk.CTkLabel(
            self.form_card,
            text="DADOS DO USUÁRIO",
            font=("Arial", 13, "bold"),
            text_color=self.COLOR_GRAY
        )

        self.form_title.pack(
            anchor="w",
            padx=25,
            pady=(25, 25)
        )

        # =========================================================
        # NOME
        # =========================================================

        self.name_label = ctk.CTkLabel(
            self.form_card,
            text="Nome completo",
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_DARK
        )

        self.name_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 7)
        )

        self.name_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Digite o nome completo",
            height=45,
            font=("Arial", 14),
            border_width=1
        )

        self.name_entry.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # =========================================================
        # MATRÍCULA
        # =========================================================

        self.registration_title = ctk.CTkLabel(
            self.form_card,
            text="Matrícula",
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_DARK
        )

        self.registration_title.pack(
            anchor="w",
            padx=25,
            pady=(0, 7)
        )

        self.registration_entry = ctk.CTkEntry(
            self.form_card,
            placeholder_text="Digite a matrícula",
            height=45,
            font=("Arial", 14),
            border_width=1
        )

        self.registration_entry.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # =========================================================
        # INSTRUÇÃO
        # =========================================================

        self.instruction_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="#F0FDF4",
            corner_radius=10
        )

        self.instruction_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        self.instruction_label = ctk.CTkLabel(
            self.instruction_frame,
            text=(
                "Mantenha o rosto centralizado\n"
                "e olhe diretamente para a câmera."
            ),
            font=("Arial", 12),
            text_color=self.COLOR_DARK_GREEN,
            justify="center"
        )

        self.instruction_label.pack(
            fill="x",
            padx=10,
            pady=14
        )

        # =========================================================
        # BOTÃO CADASTRAR
        # =========================================================

        self.capture_button = ctk.CTkButton(
            self.form_card,
            text="CAPTURAR E CADASTRAR",
            height=48,
            font=("Arial", 14, "bold"),
            fg_color=self.COLOR_GREEN,
            hover_color=self.COLOR_DARK_GREEN,
            command=self.register_user
        )

        self.capture_button.pack(
            side="bottom",
            fill="x",
            padx=25,
            pady=(10, 25)
        )

    # =============================================================
    # CÂMERA
    # =============================================================

    def update_camera(self):

        # Usa a câmera da MainWindow.
        # Não abre uma segunda webcam.

        frame = self.parent.current_frame

        if frame is not None:

            # =====================================================
            # FRAME ORIGINAL
            # =====================================================

            # Este frame NÃO é espelhado.
            # Ele será usado para gerar o embedding.
            self.current_frame = (
                frame.copy()
            )

            # =====================================================
            # DETECÇÃO
            # =====================================================

            faces = self.detector.detect(
                frame
            )

            # =====================================================
            # DISPLAY
            # =====================================================

            # Primeiro espelhamos a imagem
            # destinada à interface.
            display_frame = cv2.flip(
                frame,
                1
            )

            frame_width = (
                display_frame.shape[1]
            )

            # =====================================================
            # UM ROSTO
            # =====================================================

            if len(faces) == 1:

                self.status_label.configure(
                    text="✓ Rosto detectado",
                    text_color=self.COLOR_GREEN
                )

                x, y, w, h = (
                    faces[0]["bbox"]
                )

                # Como o display foi espelhado,
                # corrigimos a posição X.
                x_mirrored = (
                    frame_width
                    - x
                    - w
                )

                # Desenha DEPOIS do flip.
                # Assim qualquer texto futuro
                # também não ficará invertido.
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

            # =====================================================
            # MAIS DE UM ROSTO
            # =====================================================

            elif len(faces) > 1:

                self.status_label.configure(
                    text=(
                        "Mais de um rosto detectado"
                    ),
                    text_color=self.COLOR_RED
                )

                # Desenha todos os rostos
                for face in faces:

                    x, y, w, h = (
                        face["bbox"]
                    )

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
                        (0, 0, 255),
                        2
                    )

            # =====================================================
            # NENHUM ROSTO
            # =====================================================

            else:

                self.status_label.configure(
                    text=(
                        "Posicione o rosto "
                        "diante da câmera"
                    ),
                    text_color=self.COLOR_GRAY
                )

            # =====================================================
            # BGR -> RGB
            # =====================================================

            display_frame = cv2.cvtColor(
                display_frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(
                display_frame
            )

            # =====================================================
            # CUSTOMTKINTER
            # =====================================================

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(520, 390)
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

    def register_user(self):

        # =========================================================
        # CAMPOS
        # =========================================================

        name = (
            self.name_entry
            .get()
            .strip()
        )

        registration_number = (
            self.registration_entry
            .get()
            .strip()
        )

        # =========================================================
        # VALIDAÇÕES
        # =========================================================

        if not name:

            messagebox.showerror(
                "Dados incompletos",
                "Informe o nome completo.",
                parent=self
            )

            return

        if not registration_number:

            messagebox.showerror(
                "Dados incompletos",
                "Informe a matrícula.",
                parent=self
            )

            return

        if self.current_frame is None:

            messagebox.showerror(
                "Câmera",
                "Nenhuma imagem está disponível.",
                parent=self
            )

            return

        # =========================================================
        # DETECÇÃO
        # =========================================================

        faces = self.detector.detect(
            self.current_frame
        )

        if len(faces) == 0:

            messagebox.showerror(
                "Rosto não detectado",
                (
                    "Posicione o rosto diante "
                    "da câmera e tente novamente."
                ),
                parent=self
            )

            return

        if len(faces) > 1:

            messagebox.showerror(
                "Múltiplos rostos",
                (
                    "Mantenha apenas uma pessoa "
                    "diante da câmera."
                ),
                parent=self
            )

            return

        # =========================================================
        # RECORTE
        # =========================================================

        face = faces[0]

        cropped_face = (
            self.detector.crop_face(
                self.current_frame,
                face
            )
        )

        if cropped_face.size == 0:

            messagebox.showerror(
                "Erro",
                (
                    "Não foi possível processar "
                    "o rosto detectado."
                ),
                parent=self
            )

            return

        # =========================================================
        # EMBEDDING
        # =========================================================

        embedding = (
            self.embedder.generate(
                cropped_face
            )
        )

        # =========================================================
        # BANCO
        # =========================================================

        try:

            self.database.add_user(
                name,
                registration_number,
                embedding
            )

        except Exception as error:

            messagebox.showerror(
                "Erro no cadastro",
                (
                    "Não foi possível realizar "
                    "o cadastro.\n\n"
                    f"{error}"
                ),
                parent=self
            )

            return

        # =========================================================
        # SUCESSO
        # =========================================================

        messagebox.showinfo(
            "Cadastro realizado",
            (
                f"{name} foi cadastrado(a) "
                "com sucesso."
            ),
            parent=self
        )

        self.destroy()
