import bobo
import gdown
import io
import json
import pathlib
import subprocess
import urllib.parse

model_file = 'vox-cpk.pth.tar'

uploaded = pathlib.Path.cwd() / pathlib.Path('uploaded')

if not uploaded.is_dir():
    uploaded.mkdir()

if not pathlib.Path(model_file).is_file():
    id_file = '1_v_xW1V52gZCZnXgh1Ap_gwA9YVIzUnS'
    gdown.download(
        id=id_file,
        output=model_file,
        quiet=False,
        )

def do(img_path, video_path):

    subprocess.check_call(
        'python3 ../demo.py --config ../config/vox-256.yaml'
        ' --driving_video /data/.wink.mp4'
        f' --source_image "{img_path}"'
        f' --result_video "{video_path}"'
        ' --checkpoint vox-cpk.pth.tar --relative --adapt_scale',
        shell=True,
        )


@bobo.post('/model1', content_type='application/json')
def model1(bobo_request):
    '''Execute the model
    '''

    img = bobo_request.POST['test-image']

    with open(f'uploaded/{img.filename}', 'wb') as fp:
        fp.write(img.file.read())

    do(f'uploaded/{img.filename}', 'pub/generated.mp4')

    return dict(path="/pub/generated.mp4")


@bobo.post('/model2', content_type='application/json')
def model2(bobo_request):

    loc = json.loads(bobo_request.body)

    rv = []
    for img_path in loc['image_paths']:
        img_path = pathlib.Path('/data') / pathlib.Path(img_path)
        video_path = img_path.with_suffix('.mp4').as_posix()
        do(img_path.as_posix(), video_path)
        rv.append(video_path)

    return dict(video_paths=rv)


@bobo.query('/')
def index(bobo_request):
    return bobo.redirect(
        urllib.parse.urljoin(bobo_request.url, '/pub/index.html')
        )
