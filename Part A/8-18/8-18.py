import numpy as np
from cv2 import cv2
import time
from os import path
from functions import compute_motion_vector

#while loop statement.
while True:

    #menu to select action.
    print("\n Select the action you want: ")
    dialog = input(" a) Begin the Object Removal Procedure.\n b) Exit the program.\n Select either a or b option: ").lower()

    if dialog in ["a", "b"]:
    #code for a-option Begin the Object Removal Procedure.

        if dialog == "a":
            frames = 1
            filename = input("\n Give the full file name of your video (with the extension):\n ***The selected video must be in the same folder with this program.***\n")

            if path.exists(filename):
                vid = cv2.VideoCapture(filename) #get video by input's filename.
                total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) 	#counts the total number of video's frames.
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                outputfile = input("\nGive the file name of the output video: ") #name the output video.
                out = cv2.VideoWriter(outputfile+'.avi', fourcc, vid.get(5),(int(vid.get(3)), int(vid.get(4))), False)

                block_size = int(input("\nGive the macroblock size (size x size): "))
                print("\nCreating video with name \"%s\"..." % outputfile)
                start = time.time() #time calculation.

                playing, background = vid.read()  # process  the first frame (background).
                background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY) #grayscale
                background = np.pad(background, ((0, int((np.ceil(vid.get(4)/block_size) * block_size) - vid.get(4))),(0, int((np.ceil(vid.get(3)/block_size) * block_size) - vid.get(3)))),'constant', constant_values=0)
                out.write(background)
                ref = background

                print("Frame #1 of " + str(total) + " Completed.") #information message.

                #whlie loop statement for the next frames.
                while vid.isOpened():
                    playing, frame = vid.read()
                    if not playing:
                        break
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale
                    #fill the black pixels.
                    frame = np.pad(frame, ((0, int((np.ceil(vid.get(4)/block_size) * block_size) - vid.get(4))),(0, int((np.ceil(vid.get(3)/block_size) * block_size) - vid.get(3)))),'constant', constant_values=0)

                    #divide frame to macroblocks via for loop statements.
                    for i in range(0, frame.shape[0], block_size):
                        for j in range(0, frame.shape[1], block_size):
                            #compute the motion vector via outer function.
                            motion_vector = compute_motion_vector(frame[i:i+block_size, j:j+block_size], ref, (i, j), block_size)
                            if motion_vector[0] + motion_vector[1] != 0: #if motion is detected, then:
                                frame[i:i+block_size, j:j+block_size] = ref[i:i+block_size, j:j+block_size] #replace the macroblock.
                    frame = np.delete(frame, slice(int(vid.get(4)), None), 0)
                    frame = np.delete(frame, slice(int(vid.get(3)), None), 1)
                    out.write(frame)
                    frames += 1

                    print('Frame #' + str(frames) + " of " + str(total) + " Completed.") #print each completed frame number.

                vid.release()
                out.release()

                print("\nSuccess!\nThe output video, as %s.avi, has been added in your program's folder." % outputfile)
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
                        vid.release()
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
