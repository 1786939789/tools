import os

from tqdm import tqdm

from xml_util import xml_to_json
from file_util import check_dir
from image_util import plot_dir_box

def temporary_storage():
    """ temporary storage
    
    Args:

    """
    # add bboxes onto images
    txt_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/original-detect-result/face/"
    images_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/keyframe/"
    save_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/visualization/face/"

    pbar = tqdm(os.listdir(images_dir))
    for image_dir in pbar:
        pbar.set_description("Processing {}/{}".format(images_dir, image_dir))
        if not os.path.isdir(os.path.join(images_dir, image_dir)):
            continue
        txt_file = os.path.join(txt_dir, image_dir+".txt")
        check_dir(os.path.join(save_dir, image_dir))
        plot_dir_box(os.path.join(images_dir, image_dir), os.path.join(save_dir, image_dir), txt_file)

    # # add bboxes onto images
    # json_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/json_final/"
    # images_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/keyframe/"
    # save_dir = "E:/Study/data/StoryLine/TA2/kairos_data/LDC2020E33_KAIROS/visualization/face/"

    # pbar = tqdm(os.listdir(images_dir))
    # for image_dir in pbar:
    #     pbar.set_description("Processing {}/{}".format(images_dir, image_dir))
    #     if not os.path.isdir(os.path.join(images_dir, image_dir)):
    #         continue
    #     json_file = os.path.join(json_dir, image_dir+".json")
    #     check_dir(os.path.join(save_dir, image_dir))
    #     with open(json_file, "r") as f:
    #         json_data = json.load(f)
    #     image_list = os.listdir(os.path.join(images_dir, image_dir))
    #     image_list.sort()
    #     for i, image in enumerate(image_list):
    #         suffix = os.path.splitext(image)[-1]
    #         if suffix not in [".jpg", "jpeg", "png"]:
    #             continue

    #         img = cv2.imread(os.path.join(images_dir, image_dir, image))
    #         for entity in json_data["entities"]:
    #             if "label" in entity and entity["label"] == "face":
    #                 frame_index = int(entity["id"].split("-")[-3][1:])
    #                 if frame_index == i:
    #                     plot_one_box(img, entity["bbox"], entity["id"], color=(0, 0, 255))
    #         check_dir(os.path.join(save_dir, image_dir))
    #         cv2.imwrite(os.path.join(save_dir, image_dir, image), img)

if __name__ == "__main__":
    # add bboxes onto images
    txt_dir = "F:/Data/kairos/data/scenario_data/original-detect-result/ocr-2/"
    images_dir = "F:/Data/kairos/data/scenario_data/image/"
    save_dir = "F:/Data/kairos/data/scenario_data/visualization-ocr/"

    # category_list = ["obj-v", "obj-v", "obj-v", "obj-v", "obj-v", "obj-v"]

    pbar = tqdm(os.listdir(images_dir))
    for image_dir in pbar:
        pbar.set_description("Processing {}/{}".format(images_dir, image_dir))
        if not os.path.isdir(os.path.join(images_dir, image_dir)):
            continue
        txt_file = os.path.join(txt_dir, image_dir+".txt")
        check_dir(os.path.join(save_dir, image_dir))
        plot_dir_box(os.path.join(images_dir, image_dir), os.path.join(save_dir, image_dir), txt_file)
