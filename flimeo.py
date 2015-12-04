#!/usr/bin/env python
import argparse
import os
import sys


FFMPEG_BINARY_PATH = os.environ.get('FFMPEG_BINARY_PATH', "local/bin/ffmpeg")
EXTENSIONS = ['.jpeg', '.jpg', '.raw']
AGREE_MESSAGE = """You must use --agree argument.
Our recommendation is to make a copy of your pictures and work with it.
We don't want to accidentally damage your original pictures.\n"""


def get_quality(quality):
    qualities = {
        'low': 'hd480',
        'med': 'hd720',
        'hig': 'hd1080',
    }
    return qualities[quality]


def get_pics_paths(root):
    pics_paths = []
    for filename in os.listdir(root):
        filename = os.path.join(root, filename)
        name, ext = os.path.splitext(filename)
        if ext.lower() in EXTENSIONS:
            pics_paths.append(os.path.join(root, filename))

    return pics_paths


def get_paths(ipath, opath):
    ipath = os.path.abspath(ipath)
    opath = os.path.abspath(opath)
    if not os.path.exists(ipath):
        sys.stderr.write("Input path does not exists\n")
        sys.exit(1)

    if os.path.exists(opath):
        sys.stderr.write("Output path exists\n")
        sys.exit(1)
    else:
        parent = os.path.dirname(opath)
        try:
          os.makedirs(parent)
        except OSError:
          pass

    return ipath, opath


def show_estimated_duration():
    get_duration(pics_paths, fps)
    sys.stdout.write("Estimated video duration = %d\n" % duration)


def get_duration(pics_paths, fps):
    picnumber = len(pics_paths)

    return picnumber // fps


def sort_by_date(pics_paths):
    def get_creation_time(filename):
        return os.path.getmtime(filename)

    pics_paths.sort(key=get_creation_time)
    return pics_paths


def rename_files(pics_paths):
    # Rename pictures, workaround to ffmpeg bug
    # sort by creation time
    sorted_paths = sort_by_date(pics_paths)

    # name them as expected by ffmpeg
    c = 0
    pics_paths = []
    for filename in sorted_paths:
        name, ext = os.path.splitext(filename)
        root = os.path.dirname(filename)
        new_name = os.path.join(root, '%d%s' % (c, ext))
        os.rename(filename, new_name)
        pics_paths.append(new_name)
        c += 1
    return pics_paths


def create_video(ipath, opath, fps, quality):
    fps = ' -r ' + fps
    ipath = ' -i ' + os.path.join(ipath, '%d.jpg ')
    quality =' -s ' + quality
    stuff = ' -vcodec libx264 -pix_fmt yuv420p '
    stuff += ' -y '  # overwrite output files
    stuff += ' -loglevel quiet '
    command = FFMPEG_BINARY_PATH + fps + ipath + quality + stuff + opath
    os.system(command)


def main(ipath, opath, fps, quality):
    ipath, opath = get_paths(ipath, opath)
    quality = get_quality(quality)
    pics_paths = get_pics_paths(ipath)
    pics_paths = rename_files(pics_paths)
    video_path = create_video(ipath, opath, str(fps), quality)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flimeo, the best time-lapse generator *ever*')
    parser.add_argument(
        '--agree',
        help="Explicitly agree that flimeo will modify your file without guarantee",
        default=False,
        action='store_true')
    parser.add_argument('--ipath', help="path to source files")
    parser.add_argument('--opath', help="output filename")
    parser.add_argument('--fps', help="frames per second of the video", type=int, default=25)
    parser.add_argument('--quality', help="output video quality low|med|hig", type=str, default="med")
    # parser.add_argument('--ffmpeg-verbose', help="verbosity of ffmpeg")

    args = parser.parse_args()
    if not args.agree:
        sys.stderr.write(AGREE_MESSAGE)
        sys.exit(1)

    fps = args.fps
    ipath = os.path.abspath(args.ipath)
    opath = args.opath
    quality = args.quality

    main(ipath, opath, fps, quality)
