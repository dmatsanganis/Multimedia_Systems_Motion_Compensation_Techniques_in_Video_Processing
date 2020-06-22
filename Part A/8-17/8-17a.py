import numpy as np
from cv2 import cv2
import time
from os import path
from functions import entropy_calculation

#while loop statement.
while True:

    #menu to select action.
    print("\n Select the action you want: ")
    dialog = input(" a) Find whole frames difference (error frames).\n b) Exit the program.\n Select either a or b option: ").lower()

    if dialog in ["a", "b"]:
	#code for a-option error frames difference calculation.

        if dialog == "a":
            filename = input("\n Give the full file name of your video (with the extension):\n ***The selected video must be in the same folder with this program.***\n")

            if path.exists(filename):
                vid = cv2.VideoCapture(filename) #get video by input's filename.
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                outputfile = input("\nGive the file name of the output video: ") #name the output video.
                out = cv2.VideoWriter(outputfile+'.avi', fourcc, vid.get(5),(int(vid.get(3)), int(vid.get(4))), False)
                start = time.time() #time calculation

                print("\nCreating output video with name %s.avi..." % outputfile) #information message.
                playing, ref = vid.read()
                array = [] #entropy array
                ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY) #grayscale

                while vid.isOpened():
                    playing, frame = vid.read()
                    if not playing:
                        break
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale
                    error_frames = np.subtract(frame, ref)
                    array.append(error_frames.astype('int16'))
                    out.write(error_frames)
                    ref = frame
                vid.release()
                out.release()

                print("\nSuccess!\nThe output video, as %s.avi, has been added in your program's folder." % outputfile)
                print('\nEntropy: ' + str(entropy_calculation(array)))
                print('\nTime elapsed: ' + str(time.time() - start) + 's')
                #information message.

                #show the output video option.
                dialog = input("\nDo you want to play the output video? (yes/no): ").lower()
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
