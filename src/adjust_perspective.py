# import cv2
# import numpy as np

# # Cache para armazenar a matriz de transformação
# _last_field_lines = None
# _last_transform_matrix = None

# def adjust_perspective(frame, field_lines):
#     """
#     Ajusta a perspectiva do frame com base nas linhas do campo detectadas.
#     Implementa caching para evitar recálculos desnecessários.
    
#     Args:
#         frame: O frame do vídeo.
#         field_lines: Lista de linhas do campo detectadas no formato [(x1, y1, x2, y2), ...].
        
#     Returns:
#         O frame com a perspectiva corrigida.
#     """
#     global _last_field_lines, _last_transform_matrix
    
#     # Verificar se temos linhas suficientes
#     if field_lines is None or len(field_lines) < 4:
#         print("Não há linhas suficientes para ajuste de perspectiva")
#         return frame
        
#     try:
#         # Verificar se as linhas são iguais às anteriores para usar o cache
#         if (_last_field_lines is not None and 
#             len(_last_field_lines) == len(field_lines) and 
#             np.array_equal(np.array(field_lines), np.array(_last_field_lines))):
#             # Usar a matriz de transformação em cache
#             if _last_transform_matrix is not None:
#                 # Aplicar a transformação
#                 height, width = frame.shape[:2]
#                 return cv2.warpPerspective(frame, _last_transform_matrix, (width, height))
        
#         # Selecionar os 4 pontos da origem (usar apenas as 4 primeiras linhas)
#         src_pts = []
#         for i in range(min(4, len(field_lines))):
#             x1, y1, x2, y2 = field_lines[i]
#             src_pts.append([x1, y1])
#             src_pts.append([x2, y2])
        
#         # Usar apenas os 4 primeiros pontos
#         src_pts = np.array(src_pts[:4], dtype=np.float32)
        
#         # Definir os pontos de destino (retângulo)
#         height, width = frame.shape[:2]
#         dst_pts = np.array([
#             [0, 0],
#             [width, 0],
#             [0, height],
#             [width, height]
#         ], dtype=np.float32)
        
#         # Calcular a matriz de transformação
#         _last_transform_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
#         _last_field_lines = field_lines
        
#         # Aplicar a transformação
#         corrected_frame = cv2.warpPerspective(frame, _last_transform_matrix, (width, height))
        
#         return corrected_frame
        
#     except Exception as e:
#         print(f"Erro no ajuste de perspectiva: {e}")
#         return frame  # Retornar o frame original em caso de erro

import cv2
import numpy as np

# Cache to store the transformation matrix
_last_field_lines = None
_last_transform_matrix = None

def adjust_perspective(frame, field_lines):
    """
    Adjusts the perspective of the frame based on the detected field lines.
    Implements caching to avoid unnecessary recalculations.
    
    Args:
        frame: The video frame.
        field_lines: List of detected field lines in the format [(x1, y1, x2, y2), ...].
        
    Returns:
        The frame with corrected perspective.
    """
    global _last_field_lines, _last_transform_matrix
    
    # Check if we have enough lines
    if field_lines is None or len(field_lines) < 4:
        print("There are not enough lines for perspective adjustment")
        return frame
        
    try:
        # Check if the lines are the same as the previous ones to use the cache
        if (_last_field_lines is not None and 
            len(_last_field_lines) == len(field_lines) and 
            np.array_equal(np.array(field_lines), np.array(_last_field_lines))):
            # Use the cached transformation matrix
            if _last_transform_matrix is not None:
                # Apply the transformation
                height, width = frame.shape[:2]
                return cv2.warpPerspective(frame, _last_transform_matrix, (width, height))
        
        # Select the 4 source points (use only the first 4 lines)
        src_pts = []
        for i in range(min(4, len(field_lines))):
            x1, y1, x2, y2 = field_lines[i]
            src_pts.append([x1, y1])
            src_pts.append([x2, y2])
        
        # Use only the first 4 points
        src_pts = np.array(src_pts[:4], dtype=np.float32)
        
        # Define the destination points (rectangle)
        height, width = frame.shape[:2]
        dst_pts = np.array([
            [0, 0],
            [width, 0],
            [0, height],
            [width, height]
        ], dtype=np.float32)
        
        # Calculate the transformation matrix
        _last_transform_matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        _last_field_lines = field_lines
        
        # Apply the transformation
        corrected_frame = cv2.warpPerspective(frame, _last_transform_matrix, (width, height))
        
        return corrected_frame
        
    except Exception as e:
        print(f"Error in perspective adjustment: {e}")
        return frame  # Return the original frame in case of error
