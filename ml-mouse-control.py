import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import cv2
import mediapipe as mp
import tensorflow as tf
import logging
from threading import Thread
from gesture_controller import GestureController
from gesture_recognition import process_hand_landmarks, predict_gesture

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Archivo de configuración de gestos
GESTURES_CONFIG_FILE = "gestures_config.json"

class GestureRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.gestures_config = {}
        self.sensitivity = 0.9
        self.gesture_controller = GestureController()
        self.interpreter = tf.lite.Interpreter(model_path='./my_model/quantized_model.tflite')
        self.interpreter.allocate_tensors()
        self.cap = None
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Reconocimiento de Gestos")
        self.root.geometry("800x600")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        options_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opciones", menu=options_menu)
        options_menu.add_command(label="Configurar Gestos", command=self.configure_gestures_gui)
        options_menu.add_command(label="Calibrar Sensibilidad", command=self.calibrate_sensitivity)
        options_menu.add_command(label="Ayuda", command=self.show_help)
        options_menu.add_separator()
        options_menu.add_command(label="Salir", command=self.quit_app)

        self.video_label = ttk.Label(self.root)
        self.video_label.pack(expand=True, fill=tk.BOTH)

        self.start_button = ttk.Button(self.root, text="Iniciar", command=self.start_recognition)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Detener", command=self.stop_recognition, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

    def configure_gestures_gui(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuración de Gestos")
        config_window.geometry("400x300")

        actions = {
            "0": "Clic Derecho",
            "1": "Zoom",
            "2": "Desplazamiento Vertical",
            "3": "Cambio de Ventana",
            "4": "Clic Izquierdo",
            "5": "Doble Clic",
            "6": "Control de Volumen"
        }

        gesture_vars = {}
        for code, action in actions.items():
            frame = ttk.Frame(config_window)
            frame.pack(pady=5)
            label = ttk.Label(frame, text=f"{action}:")
            label.pack(side=tk.LEFT, padx=5)
            var = tk.StringVar(value=self.gestures_config.get(code, ""))
            gesture_vars[code] = var
            entry = ttk.Entry(frame, textvariable=var)
            entry.pack(side=tk.LEFT)

        save_button = ttk.Button(config_window, text="Guardar", command=lambda: self.save_gestures_config(gesture_vars, config_window))
        save_button.pack(pady=10)

    def save_gestures_config(self, gesture_vars, config_window):
        for code, var in gesture_vars.items():
            if var.get():
                self.gestures_config[code] = var.get()
        try:
            with open(GESTURES_CONFIG_FILE, 'w') as f:
                json.dump(self.gestures_config, f, indent=4)
            logging.info("Configuración de gestos guardada correctamente.")
            messagebox.showinfo("Configuración guardada", "La configuración de gestos ha sido guardada.")
            config_window.destroy()
        except IOError as e:
            logging.error(f"Error al guardar la configuración de gestos: {e}")
            messagebox.showerror("Error", "No se pudo guardar la configuración de gestos.")

    def calibrate_sensitivity(self):
        sensitivity = simpledialog.askfloat("Calibrar Sensibilidad", "Ingrese el umbral de confianza (0.1 a 1.0):", minvalue=0.1, maxvalue=1.0)
        if sensitivity is not None:
            self.sensitivity = sensitivity
        else:
            logging.error("Valor de sensibilidad no válido. Usando valor predeterminado (0.9).")
            self.sensitivity = 0.9

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda")
        help_window.geometry("400x300")

        help_text = """
        Bienvenido al sistema de reconocimiento de gestos.
        - Gesto 0: Clic Derecho
        - Gesto 1: Zoom
        - Gesto 2: Desplazamiento Vertical
        - Gesto 3: Cambio de Ventana
        - Gesto 4: Clic Izquierdo
        - Gesto 5: Doble Clic
        - Gesto 6: Control de Volumen
        """
        help_label = ttk.Label(help_window, text=help_text, justify=tk.LEFT)
        help_label.pack(pady=20)

    def start_recognition(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            logging.error("No se pudo abrir la cámara.")
            return

        self.recognition_thread = Thread(target=self.run_recognition)
        self.recognition_thread.start()

    def stop_recognition(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def run_recognition(self):
        with mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7) as hands:
            while self.running and self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    logging.error("No se pudo capturar la imagen.")
                    break

                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        points = process_hand_landmarks(hand_landmarks.landmark, image.shape)
                        state, confidence = predict_gesture(self.interpreter, hand_landmarks.landmark)  # Corregido aquí

                        if confidence > self.sensitivity:
                            configured_gesture = self.gestures_config.get(str(state), None)
                            if configured_gesture:
                                self.gesture_controller.handle_gesture(configured_gesture)
                                cv2.putText(image, f"Gesto: {configured_gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            else:
                                cv2.putText(image, f"Gesto no configurado: {state}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow('Gesture Recognition', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.stop_recognition()

    def quit_app(self):
        self.stop_recognition()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureRecognitionApp(root)
    root.mainloop()