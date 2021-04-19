import sys
import argparse
from yolo import YOLO, detect_video
from PIL import Image
import os, glob, cv2
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def detect_img2(yolo):
    dir = "VOC2007/9_14/0915/"
    #ls = os.listdir("VOC2007/9_14/0915")
    ls = ['5','6','7','25','26','27','34','44']
    for name in ls:
        path = dir + name + '/'
        outdir = dir + name + '_out/'
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        list = os.listdir(path)
        list.sort()
        txt_name = dir + name + '.txt'
        f = open(txt_name, "w")
        for jpgfile in list:
            f.write(jpgfile)
            img = Image.open(path+jpgfile)
            img = yolo.detect_image(img, f)
            f.write('\n')
            img.save(os.path.join(outdir, jpgfile))
    yolo.close_session()
    f.close()
def detect_img3(yolo):
    dir = "VOC2007/test2.0/"
    out_dir = "VOC2007/out_test2.0/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    ls = os.listdir(dir)
    #list.sort()
    txt_name = "VOC2007/res_test2.0.txt"
    f = open(txt_name, "w")
    for name in ls:
        f.write(name)
        img_path = dir + name
        img = Image.open(img_path)
        img = yolo.detect_image(img, f)
        f.write('\n')
        img.save(out_dir+name)
    yolo.close_session()
    f.close()
def detect_img1(yolo):
    dir = "VOC2007/test2.0/"
    out_dir = "VOC2007/out_test2.0/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    ls = os.listdir(dir)
    #list.sort()
    txt_name = "VOC2007/res_test2.0.txt"
    f = open(txt_name, "w")
    for name in ls:
        f.write(name)
        img_path = dir + name
        image = cv2.imread(img_path)
        img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # img = Image.open(img_path)
        img = yolo.detect_image(img, f)
        f.write('\n')
        img.save(out_dir+name)
    yolo.close_session()
    f.close()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model', type=str,
        help='path to model weight file, default ' + YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' + YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' + YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' + str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode, will ignore all positional arguments'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str,required=False,default='./path2your_video',
        help = "Video input path"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help = "[Optional] Video output path"
    )

    FLAGS = parser.parse_args()

    if FLAGS.image:
        """
        Image detection mode, disregard any remaining command line arguments
        """
        print("Image detection mode")
        if "input" in FLAGS:
            print(" Ignoring remaining command line arguments: " + FLAGS.input + "," + FLAGS.output)
        detect_img1(YOLO(**vars(FLAGS)))
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
