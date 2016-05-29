#!/usr/bin/env python
import argparse
import os
import sys


FFMPEG_BINARY_PATH = os.environ.get('FFMPEG_BINARY_PATH', "local/bin/ffmpeg")
EXTENSIONS = ['.jpeg', '.jpg', '.raw']
QUALITIES = {
    'low': 'hd480',
    'med': 'hd720',
    'hig': 'hd1080',
}


def get_quality(quality):
    return QUALITIES[quality]


def get_pics_paths(root):
    pics_paths = []
    for filename in os.listdir(root):
        filename = os.path.join(root, filename)
        name, ext = os.path.splitext(filename)
        if ext.lower() in EXTENSIONS:
            pics_paths.append(os.path.join(root, filename))

    return pics_paths


def get_input_path(input_path):
    input_path = os.path.abspath(input_path)
    if not os.path.exists(input_path):
        sys.stderr.write("flimeo: Input path does not exists\n")
        sys.exit(1)

    return input_path


def get_output_path(output_path):
    output_path = os.path.abspath(output_path)

    if os.path.exists(output_path):
        sys.stderr.write("flimeo: Output path exists\n")
        sys.exit(1)
    else:
        parent = os.path.dirname(output_path)
        try:
          os.makedirs(parent)
        except OSError:
          pass

    return output_path


def get_paths(input_path, output_path):
    input_path = get_input_path(input_path)
    output_path = get_output_path(output_path)

    return input_path, output_path


def get_duration(pics_paths, fps):
    picnumber = len(pics_paths)

    return picnumber / fps


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
        ext = ext.lower()
        root = os.path.dirname(filename)
        new_name = os.path.join(root, '%d%s' % (c, ext))
        os.rename(filename, new_name)
        pics_paths.append(new_name)
        c += 1
    return pics_paths


def create_video(input_path, output_path, fps, quality):
    fps = ' -r ' + fps
    input_path = ' -i ' + os.path.join(input_path, '%d.jpg ')
    quality =' -s ' + quality
    stuff = ' -vcodec libx264 -pix_fmt yuv420p '
    stuff += ' -y '  # overwrite output files
    stuff += ' -loglevel quiet '
    command = FFMPEG_BINARY_PATH + fps + input_path + quality + stuff + output_path
    os.system(command)


def show_estimated_duration(options):
    input_path = get_input_path(options.input_path)
    pics_paths = get_pics_paths(input_path)
    duration = get_duration(pics_paths, options.fps)
    sys.stdout.write("flimeo: Estimated video duration at {} fps = {} seconds\n".format(options.fps, duration))


def main(options):
    input_path, output_path = get_paths(options.input_path, options.output_path)
    quality = get_quality(options.quality)
    pics_paths = get_pics_paths(input_path)
    pics_paths = rename_files(pics_paths)
    video_path = create_video(input_path, output_path, str(options.fps), quality)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Flimeo', description='The best time-lapse generator *ever*')

    subparsers = parser.add_subparsers()

    parser_a = subparsers.add_parser('get-duration', help='Get the estimated duration of the output video in seconds')
    parser_a.add_argument('--fps', help="frames per second of the video", type=int, default=25)
    parser_a.add_argument('input_path', help="path to source files")
    parser_a.set_defaults(func=show_estimated_duration)

    parser_b = subparsers.add_parser('make-video', help='Make the video')
    parser_b.add_argument('--fps', help="frames per second of the video", type=int, default=25)
    parser_b.add_argument('--quality', help="output video quality", choices=QUALITIES.keys(), type=str, default="med")
    parser_b.add_argument('input_path', help="path to source files")
    parser_b.add_argument('output_path', help="output filename")
    parser_b.set_defaults(func=main)

    args = parser.parse_args()
    args.func(args)
