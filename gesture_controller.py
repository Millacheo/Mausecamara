import pyautogui
import logging

class GestureController:
    def __init__(self):
        logging.info("GestureController inicializado.")
    
    def handle_gesture(self, gesture_name):
        """
        Maneja las acciones asociadas a un gesto.
        :param gesture_name: Nombre del gesto configurado.
        """
        try:
            if gesture_name == "Clic Derecho":
                self.right_click()
            elif gesture_name == "Zoom":
                self.zoom()
            elif gesture_name == "Desplazamiento Vertical":
                self.scroll_vertical()
            elif gesture_name == "Cambio de Ventana":
                self.switch_window()
            elif gesture_name == "Clic Izquierdo":
                self.left_click()
            elif gesture_name == "Doble Clic":
                self.double_click()
            elif gesture_name == "Control de Volumen":
                self.volume_control()
            else:
                logging.warning(f"Gesto no reconocido: {gesture_name}")
        except Exception as e:
            logging.error(f"Error al manejar el gesto '{gesture_name}': {e}")

    def right_click(self):
        """Realiza un clic derecho."""
        logging.info("Ejecutando: Clic Derecho")
        pyautogui.rightClick()

    def zoom(self):
        """Simula un zoom (puede personalizarse)."""
        logging.info("Ejecutando: Zoom")
        pyautogui.hotkey('ctrl', '+')

    def scroll_vertical(self):
        """Simula un desplazamiento vertical."""
        logging.info("Ejecutando: Desplazamiento Vertical")
        pyautogui.scroll(-100)

    def switch_window(self):
        """Cambia de ventana."""
        logging.info("Ejecutando: Cambio de Ventana")
        pyautogui.hotkey('alt', 'tab')

    def left_click(self):
        """Realiza un clic izquierdo."""
        logging.info("Ejecutando: Clic Izquierdo")
        pyautogui.click()

    def double_click(self):
        """Realiza un doble clic."""
        logging.info("Ejecutando: Doble Clic")
        pyautogui.doubleClick()

    def volume_control(self):
        """Aumenta o disminuye el volumen."""
        logging.info("Ejecutando: Control de Volumen")
        pyautogui.press('volumeup')  # Puedes cambiar esto según tus necesidades