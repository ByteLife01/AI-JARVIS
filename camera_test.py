import cv2

print("Testing Camera... (Press 'q' to quit)")
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Camera not found!")
        break
        
    cv2.imshow("JARVIS VISION TEST", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()