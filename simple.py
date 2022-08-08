import itertools
import cv2
import mediapipe as mp
import time
import pyautogui


COLOR = (0, 0, 255) # RED COLOR

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600) # my laptop width size
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)  # my laptop height size

hands = mp_hands.Hands(model_complexity=0, min_detection_confidence=0.8, min_tracking_confidence=0.8)

while cap.isOpened():
    _, image = cap.read()
    image = cv2.flip(image,1)
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        height, width,_ = image.shape  #480 640
        #print(height,width)
        annotated_image = image.copy()
        for hands_landmarks in result.multi_hand_landmarks:
            wrist_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.WRIST].x*width*2.5)
            wrist_y = int(hands_landmarks.landmark[mp_hands.HandLandmark.WRIST].y*height*1.875)
            index_finger_mcp_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x*width*2.5)
            index_finger_mcp_y = int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y*height*1.875)
            center_x = (wrist_x+index_finger_mcp_x)//2
            center_y = (wrist_y+index_finger_mcp_y)//2
            cv2.circle(image, (int(center_x / 2.5), int(center_y / 1.875)), 1, COLOR, 7)
            wrist_coor = (int(center_x / 2.5), int(center_y / 1.875))
            center_y = center_y - 400
            center_x = center_x - 400
            index_finger_top_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x*width)
            index_finger_top_y= int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y*height)
            index_finger_dip_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x * width)
            index_finger_dip_y = int(hands_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * height)
            cv2.line(image, (index_finger_top_x, index_finger_top_y), (index_finger_dip_x, index_finger_dip_y), COLOR, 1)
            cv2.circle(image, (index_finger_dip_x,index_finger_dip_y), 1, COLOR, 3)
            cv2.circle(image, (index_finger_top_x, index_finger_top_y), 1, COLOR, 3)
            middle_finger_top_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
            middle_finger_top_y = int(hands_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)
            cv2.circle(image, (middle_finger_top_x, middle_finger_top_y), 1, COLOR, 3)
            middle_finger_dip_x = int(hands_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].x * width)
            middle_finger_dip_y = int(hands_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * height)
            cv2.circle(image, (middle_finger_dip_x, middle_finger_dip_y), 1, COLOR, 3)
            cv2.line(image, (middle_finger_top_x, middle_finger_top_y), (middle_finger_dip_x, middle_finger_dip_y), COLOR, 1)
            cv2.line(image, (middle_finger_top_x, middle_finger_top_y), wrist_coor,
                     COLOR, 1)
            cv2.line(image, (index_finger_top_x, index_finger_top_y), wrist_coor,
                     COLOR, 1)
            if center_x >=0 and center_x <= 1600 and center_y>=0 and center_y <=900:
                pyautogui.moveTo(center_x, center_y)
                if index_finger_top_y > index_finger_dip_y:
                    COLOR = (255,0,0)
                    cv2.putText(image,  "Left Click",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1, COLOR, 8)
                    print('left click')
                    pyautogui.dragTo(button='left')
                    #pyautogui.click(center_x, center_y)
                elif middle_finger_top_y > middle_finger_dip_y:
                    print("right clicl")
                    COLOR = (255, 0, 0)
                    pyautogui.dragTo(button='right')
                    cv2.putText(image, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1, COLOR, 8)

                    #pyautogui.click(center_x,center_y, button='right')
                else:
                    COLOR = (0,0,255)



    #image = cv2.resize(image, (1600,900))
    cv2.imshow("Hands Experiment:", image)
    if cv2.waitKey(5)& 0xFF == 27:
        break
cap.release()