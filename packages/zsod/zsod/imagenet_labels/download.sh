# Full category names, several for one class (synsets)
# https://gist.github.com/yrevar/942d3a0ac09ec9e5eb3a
wget -O synsets.txt https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/raw/238f720ff059c1f82f368259d1ca4ffa5dd8f9f5/imagenet1000_clsidx_to_labels.txt

# First name from each synset
# Link from here https://github.com/anishathalye/imagenet-simple-labels
wget -O first.json https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json

# Simple labels, may be more common
# https://github.com/anishathalye/imagenet-simple-labels
wget -O simple.json https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json

# Grouped labels, ex: Samoyed, Brittany_spaniel -> dogs
# https://github.com/noameshed/novelty-detection/blob/master/imagenet_categories.csv
wget -O groups.csv https://raw.githubusercontent.com/noameshed/novelty-detection/master/imagenet_categories.csv