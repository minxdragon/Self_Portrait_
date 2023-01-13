import cv2

# Open a window with the default camera
cap = cv2.VideoCapture(0)

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret==True:
        # Write the frame to the VideoWriter object
        out.write(frame)
        # Display the frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #close window after 30 seconds
            cv2.waitKey(30000)
            break
    else:
        break

