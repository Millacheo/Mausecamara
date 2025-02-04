import numpy as np
import logging

def process_hand_landmarks(landmarks, image_shape):
    """
    Procesa los puntos de referencia de la mano para normalizarlos.
    :param landmarks: Lista de puntos de referencia de la mano.
    :param image_shape: Dimensiones de la imagen (alto, ancho).
    :return: Lista de puntos normalizados.
    """
    height, width = image_shape[:2]
    points = []
    for landmark in landmarks:
        points.append(landmark.x * width)
        points.append(landmark.y * height)
        points.append(landmark.z * width)  # Coordenada z (profundidad)
    return points

def predict_gesture(interpreter, landmarks):
    """
    Predice el gesto utilizando el modelo TFLite.
    :param interpreter: Intérprete TFLite cargado.
    :param landmarks: Lista de puntos de referencia de la mano.
    :return: (estado, confianza) - Estado del gesto y su confianza.
    """
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocesar los puntos de referencia
    input_data = np.array([landmarks], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtener la salida del modelo
    output_data = interpreter.get_tensor(output_details[0]['index'])
    state = np.argmax(output_data)
    confidence = output_data[0][state]

    logging.info(f"Gesto predicho: {state}, Confianza: {confidence}")
    return state, confidence