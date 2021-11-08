import bobo
import io
import subprocess


@bobo.post('/do', content_type='application/json')
def do(bobo_request):
    '''Execute the model

    '''
    img = bobo_request.POST['test-image']
    with open(f'uploaded/{img.filename}', 'wb') as fp:
        fp.write(img.file.read())

    subprocess.check_call(
        'python3 demo.py --config config/vox-256.yaml'
        ' --driving_video driving-video/video.mp4'
        f' --source_image uploaded/{img.filename}'
        '--result_video pub/generated.mp4'
        ' --checkpoint vox-cpk.pth.tar --relative --adapt_scale',
        shell=True
        )

    # It returns the path of the video
    return dict(path="/pub/generated.mp4")

@bobo.query('/')
def index():
    return 'hola'
