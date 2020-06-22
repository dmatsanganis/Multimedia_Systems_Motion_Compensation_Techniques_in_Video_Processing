import numpy as np
from cv2 import cv2
import time
from os import path
from functions import compute_motion_vector, entropy_calculation

#while loop statement.
while True:

    #menu to select action.
    print("\n Select the action you want: ")
    dialog = input(" a) Find blocks difference (motion prediction method).\n b) Exit the program.\n Select either a or b option: ").lower()

    if dialog in ["a", "b"]:
    #code for a-option motion prediction difference calculation.

        if dialog == "a":
            frames = 1
            filename = input("\n Give the full file name of your video (with the extension):\n ***The selected video must be in the same folder with this program.***\n")

            if path.exists(filename):
                vid = cv2.VideoCapture(filename) #get video by input's filename.
                total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) 	#counts the total number of video's frames.
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                outputfile = input("\nGive the file name of the output video: ") #name the output video.
                out = cv2.VideoWriter(outputfile+'.avi', fourcc, vid.get(5),(int(vid.get(3)), int(vid.get(4))), False)
                start = time.time() #time calculation

                print("\nCreating output video with name %s.avi..." % outputfile) #information message.
                playing, ref = vid.read()
                ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY) #grayscale
                #fill the black pixels.
                ref = np.pad(ref, ((0, int((np.ceil(vid.get(4)/16) * 16) - vid.get(4))),(0, int((np.ceil(vid.get(3)/16) * 16) - vid.get(3)))),'constant', constant_values=0)
                array = [] #entropy array.

                print("Frame #1 of " + str(total) + " Completed.") #information message.

                #whlie loop statement for the next frames.
                while vid.isOpened():
                    playing, frame = vid.read()
                    if not playing:
                        break
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale
                    #fill the black pixels.
                    frame = np.pad(frame, ((0, int((np.ceil(vid.get(4)/16) * 16) - vid.get(4))),(0, int((np.ceil(vid.get(3)/16) * 16) - vid.get(3)))),'constant', constant_values=0)
                    temp = np.zeros((ref.shape[0], ref.shape[1]), dtype=np.uint8)

                    #divide frame to macroblocks via for loop statements.
                    for i in range(0, frame.shape[0], 16):
                        for j in range(0, frame.shape[1], 16):
                            motion_vector = compute_motion_vector(frame[i:i+16, j:j+16], ref, (i, j))
							#compute the motion vector via outer function.
                            cv2.subtract(frame[i:i + 16, j:j + 16], ref[i + motion_vector[0]:i + 16 + motion_vector[0], j + motion_vector[1]:j + 16 + motion_vector[1]], temp[i:i+16, j:j+16])
                    ref = frame
                    temp = np.delete(temp, slice(int(vid.get(4)), None), 0)
                    temp = np.delete(temp, slice(int(vid.get(3)), None), 1)
                    array.append(temp.astype('int16'))
                    out.write(temp)
                    frames += 1

                    print('Frame #' + str(frames) + " of " + str(total) + " Completed.") #print each completed frame number.

                vid.release()
                out.release()

                print("\nSuccess!\nThe output video, as %s.avi, has been added in your program's folder." % outputfile)
                print('\nEntropy: ' + str(entropy_calculation(array)))
                print('\nTime elapsed: ' + str(time.time() - start) + 's')
                #information message.

                #show the output video option.
                dialog = input("\nDo you want to play the video? (yes/no): ").lower()
                if dialog in ["yes", "no"]:
                    if dialog == "yes":
                        vid = cv2.VideoCapture(outputfile+'.avi') #find the output video by name.
                        while vid.isOpened():
                            playing, frame = vid.read()
                            if not playing:
                                break
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale
                            cv2.imshow('Video Playback', frame)
                            if cv2.waitKey(int(vid.get(5))) & 0xFF == ord('q'):
                                break
                        vid.read()
                        cv2.destroyAllWindows()
                        continue
                    if dialog == "no":
                        continue
                else:
                    print("\nInvalid input, the video will not play.") #error (invalid name input) message.
                    continue
            else:
                print("\nFile does not exist. Please try again.") #error (file not exist) message.

	#code for b-option (exit the program).
        if dialog == "b":
            input("\nPress Enter to exit...")
            break
    else:
        print("\nInvalid input, please try again.")  #error (invalid name input) message.
