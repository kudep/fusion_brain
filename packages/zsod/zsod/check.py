
from PIL import Image

from .pipeline import search_on_image

def labeled_img2box(img, label):
    try:
        img_path = img
        image = Image.open(img_path)
        results_local = search_on_image(image, [label])
        results = [list(region.to_xywh()) for region in results_local]
    except Exception as exc:
        print(f"exc={exc}")
        results = []
    return results


# cur_dir = pathlib.Path(__file__).parent
# results = {}
# for img, labels in {"dog.jpg": ['dog', 'кот']}.items():
#     results.update(predict_zsod(cur_dir /img , labels))
# print(f"results={results}")
