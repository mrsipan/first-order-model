import bobo
import io
import json
import pathlib
import subprocess


def do(img_path, video_path):

    subprocess.check_call(
        'python3 ../demo.py --config ../config/vox-256.yaml'
        ' --driving_video driving-video/wink.mp4'
        f' --source_image "{img_path}"'
        ' --result_video "{video_path}"'
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

    do('upload/{img.filename}', 'pub/generated.mp4')

    return dict(path="/pub/generated.mp4")


@bobo.post('/model2', content_type='application/json')
def model2(bobo_request):

    loc = json.loads(bobo_request.body)

    rv = []
    for img_path in loc['image_paths']:
        img_path = pathlib.Path('/data') / pathlib.Path('img_path')
        video_path = img_path.with_suffix('.mp4').as_posix()
        do(img_path.as_posix(), video_path)
        rv.append(video_path)

    return dict(video_paths=rv)


@bobo.query('/')
def index(bobo_request):
    return bobo.redirect(bobo_request.url + '/pub/index.html')
