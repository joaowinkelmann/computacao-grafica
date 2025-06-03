
# carregar uma imagem
# converter a imagem para escala de cinza
# adicionar uma borda na imagem com o fundo branco ou preto
# fazer os mesmo processos com um vídeo

import cv2

def main():
    img = cv2.imread("imagem.webp")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    # pega as dimensões da imagem
    img_x = img.shape[0]
    img_y = img.shape[1]
    
    # tamanho da borda
    border = 10
    border_color = 0 # preto
    
    # vamos fazer um for para adicionar uma borda
    for x in range(img_x):
        for y in range(img_y):
            if x < border or x >= img_x - border or y < border or y >= img_y - border:
                img[x][y] = border_color

    cv2.imshow("Imagem com borda", img)
    cv2.waitKey(0)
   
def carregar_video():
    video = cv2.VideoCapture("video.mkv")
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # converter o frame para escala de cinza
        frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # adicionar borda
        frame_cinza = cv2.copyMakeBorder(frame_cinza, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[0])
        
        cv2.imshow("Vídeo", frame_cinza)
        
    

if __name__ == "__main__":
    # main()
    carregar_video()
    