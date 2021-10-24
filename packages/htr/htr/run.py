import pathlib

from .model import Model, DecoderType
from .main_fb import FilePaths, predict

data_dir = pathlib.Path("/htr_data")


decoder_mapping = {
    "bestpath": DecoderType.BestPath,
    "beamsearch": DecoderType.BeamSearch,
    "wordbeamsearch": DecoderType.WordBeamSearch,
}

decoder_type = decoder_mapping["bestpath"]

model = Model(list(open(FilePaths.fn_char_list).read()), decoder_type, must_restore=True, dump=False)


image = str((data_dir / "data/img.png").absolute())
min_confidence = 0


def img2text(img):
    try:
        return predict(model, fn_img=img).get("recognized", "")
    except Exception as exc:
        print(exc)
        return ""
