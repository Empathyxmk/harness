import pytest

def get_2010_test_image_ids():
    # Public version: for synthetic test, return a list of identifiers
    return ['img001', 'img002', 'img003']

def test_2010_from_2012_processing(tmp_path):
    year = '2010'
    testset = 'test'

    VOCdevkit2012 = './datasets/VOCdevkit2012'
    VOCdevkit2010 = './datasets/VOCdevkit2010'

    # Fake imdb_from_voc: returns object with .details.VOCopts.detrespath and .details.VOCopts.classes
    class Details:
        def __init__(self):
            self.VOCopts = type('VOCopts', (), {})()
            self.VOCopts.detrespath = str(tmp_path / "%s_det_test_%s.txt")
            self.VOCopts.classes = ['cat', 'dog']
    class Imdb:
        def __init__(self):
            self.details = Details()
    imdb_2012 = Imdb()

    image_ids_2010 = get_2010_test_image_ids()
    detrespath_2010 = str(tmp_path / '%s_det_test_%s.txt')
    detrespath_2012 = imdb_2012.details.VOCopts.detrespath

    id_map = {i: True for i in image_ids_2010}

    # Create dummy test data for .txt file, one file per class
    for cls in imdb_2012.details.VOCopts.classes:
        res_fn = detrespath_2012 % ('comp4', cls)
        # Write a dummy detres 2012 file
        with open(res_fn, 'w') as f:
            if cls == 'cat':
                f.write("img001 1.23 10 20 30 40\n")
                f.write("img999 0.99 15 25 35 45\n")  # not in 2010 set
            else:
                f.write("img002 2.34 11 21 31 41\n")
                f.write("img003 1.00 12 22 32 42\n")

    # For every class, filter image ids by presence in 2010 set
    for cls in imdb_2012.details.VOCopts.classes:
        res_fn_2012 = detrespath_2012 % ('comp4', cls)
        with open(res_fn_2012, 'r') as f:
            lines = f.readlines()
        parsed = []
        for line in lines:
            tokens = line.strip().split()
            if len(tokens) == 6:
                imgid = tokens[0]
                if imgid in id_map:
                    parsed.append(line.strip())
        # Write out filtered to detrespath_2010
        res_fn_2010 = detrespath_2010 % ('comp4', cls)
        with open(res_fn_2010, 'w') as f:
            for p in parsed:
                f.write(p + "\n")
        # Check file content is correct
        with open(res_fn_2010) as f:
            keep_lines = [l.strip().split()[0] for l in f.readlines()]
            assert all(k in image_ids_2010 for k in keep_lines)