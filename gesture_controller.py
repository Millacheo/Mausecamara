class GestureController:
    def handle_gesture(self, gesture):
        """
        Maneja un gesto detectado y realiza la acción correspondiente.
        """
        if gesture == "Clic Derecho":
            print("Simulando clic derecho")
        elif gesture == "Clic Izquierdo":
            print("Simulando clic izquierdo")
        elif gesture == "Zoom":
            print("Simulando zoom")
        elif gesture == "Desplazamiento Vertical":
            print("Simulando desplazamiento vertical")
        elif gesture == "Cambio de Ventana":
            print("Simulando cambio de ventana")
        elif gesture == "Doble Clic":
            print("Simulando doble clic")
        elif gesture == "Control de Volumen":
            print("Simulando control de volumen")
        else:
            print(f"Gesto no reconocido: {gesture}")
