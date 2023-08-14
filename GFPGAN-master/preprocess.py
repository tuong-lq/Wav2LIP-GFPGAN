import cv2
from tqdm import tqdm
from os import path

import os

outputPath = '/home/ubuntu/Wav2Lip-GFPGAN/outputs'
inputAudioPath = '/home/ubuntu/Wav2Lip-GFPGAN/lipsync_audio_1.wav'
def get_frames():
    inputVideoPath = '/home/ubuntu/Wav2Lip-GFPGAN/outputs/result_voice.mp4'
    unProcessedFramesFolderPath = '/home/ubuntu/Wav2Lip-GFPGAN/outputs/frames'

    if not os.path.exists(unProcessedFramesFolderPath):
        os.makedirs(unProcessedFramesFolderPath)

    vidcap = cv2.VideoCapture(inputVideoPath)
    numberOfFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print("FPS: ", fps, "Frames: ", numberOfFrames)

    for frameNumber in tqdm(range(numberOfFrames)):
        _,image = vidcap.read()
        cv2.imwrite(path.join(unProcessedFramesFolderPath, str(frameNumber).zfill(4)+'.jpg'), image)

def resolution():
    restoredFramesPath =  '/home/ubuntu/Wav2Lip-GFPGAN/outputs/restored_imgs/'
    processedVideoOutputPath = '/home/ubuntu/Wav2Lip-GFPGAN/outputs'

    dir_list = os.listdir(restoredFramesPath)
    dir_list.sort()
    batch = 0
    batchSize = 300
    for i in tqdm(range(0, len(dir_list), batchSize)):
        img_array = []
        start, end = i, i+batchSize
        print("processing ", start, end)
        for filename in  tqdm(dir_list[start:end]):
            filename = restoredFramesPath+filename;
            img = cv2.imread(filename)
            if img is None:
                continue
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)


        out = cv2.VideoWriter(processedVideoOutputPath+'/batch_'+str(batch).zfill(4)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
        batch = batch + 1
        
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()

    concatTextFilePath = outputPath + "/concat.txt"
    concatTextFile=open(concatTextFilePath,"w")
    for ips in range(batch):
        concatTextFile.write("file batch_" + str(ips).zfill(4) + ".avi\n")
        concatTextFile.close()

        concatedVideoOutputPath = outputPath + "/concated_output.avi"
        os.system(f'ffmpeg -y -f concat -i {concatTextFilePath} -c copy {concatedVideoOutputPath}')

        finalProcessedOuputVideo = processedVideoOutputPath+'/final_with_audio.avi'
        os.system(f'ffmpeg -y -i {concatedVideoOutputPath} -i /home/ubuntu/Wav2Lip-GFPGAN/lipsync_audio_1.wav -c:v copy -c:a aac {finalProcessedOuputVideo}')

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input = avi_file_path, output = output_name))
    return True

#get_frames()
#resolution()
convert_avi_to_mp4('/home/ubuntu/Wav2Lip-GFPGAN/outputs/final_with_audio.avi', '/home/ubuntu/Wav2Lip-GFPGAN/outputs/final_with_audio_jp.mp4')
