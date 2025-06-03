import cv2

def main():
    # cv2.imshow("Hello OpenCV", cv2.imread("aaaaaaaa.webp"))
    
    ## alterar de BGR para RGB
    # img = cv2.imread("aaaaaaaa.webp")
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    ## aterar para escala de cinza
    img = cv2.imread("imagem.webp")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    cv2.imshow("Hello OpenCV", img)
    
    
main()
cv2.waitKey(0)