import cv2, click, tqdm
import numpy as np

import os


def absoluteFilePaths(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            basepath = os.path.abspath(os.path.join(dirpath, f))
            if "ground-truth" not in basepath:
                yield basepath


def process_video(filename, basedir, ID):
    print(filename, basedir, ID)
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        print(f"Error opening video stream {filename}")

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            if count % 24 == 0:
                export_file = (
                    os.path.abspath(os.path.join(basedir, str(ID * 10 + count // 24))) + ".jpg"
                )
                print("writing", export_file)
                cv2.imwrite(export_file, frame)
        else:
            break
        count += 1


@click.command()
@click.argument("video_src_dirs")
@click.argument("export_dir")
def main(video_src_dirs, export_dir):
    try:
        os.mkdir(export_dir)
    except:
        pass

    ID = 0
    for file in absoluteFilePaths(video_src_dirs):
        if file.endswith(".mp4"):
            process_video(file, export_dir, ID)
            ID += 1


if __name__ == "__main__":
    main()
