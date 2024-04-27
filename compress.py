import os
import gzip
import shutil

input = "your target folder"
#change the extension to fit your purposes
ext = ".gz"
for i in os.listdir(input):
    seg_path = os.path.join(input, i)
    with open(seg_path, 'rb') as f_in:
        name = i+ext
        with gzip.open(os.path.join(input, name), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            os.remove(seg_path)
            