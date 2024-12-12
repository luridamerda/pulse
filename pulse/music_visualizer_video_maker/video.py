import librosa
import ffmpeg
import multiprocessing
import moviepy.editor as mpy
import gizeh as gz

from pulse.music_visualizer_video_maker.options import Options

class Video:
    def __init__(self, audioFile, output):
        self.Audio = mpy.AudioFileClip(audioFile)
        self.Output = output
        self.Duration = int(self.Audio.duration)
        self.MainSurface = gz.Surface(Options.WIDTH, Options.HEIGHT, bg_color=(0, 0, 1, 0))


    def Show(self, drawable, **kwargs): 
        return mpy.VideoClip(lambda t: drawable(t, **kwargs), duration=self.Duration, ismask=False)

    def ShowTransparent(self, drawable, **kwargs): 
        clipMask = mpy.VideoClip(lambda t: drawable(t, **kwargs)[:, :, 3] / 255.0, duration=self.Duration, ismask=True)
        return mpy.VideoClip(lambda t: drawable(t, **kwargs)[:, :, :3], duration=self.Duration).set_mask(clipMask)

    def Generate(self, videoElems):
        video = mpy.CompositeVideoClip(videoElems, size=(Options.WIDTH, Options.HEIGHT)).set_duration(self.Duration)
        video = video.set_audio(self.Audio)
        video.write_videofile(self.Output, fps=Options.FPS, threads=multiprocessing.cpu_count())



    # self, time, text, surfaceSize, xy, color, fontSize, fontWeight, font
    def RenderText(self, time, **kwargs):
        #surface = gz.Surface(kwargs["surfaceW"], kwargs["surfaceH"], bg_color=(0, 0, 1, 0))
        text = gz.text(kwargs["text"], fontfamily=kwargs["fontfamily"], fontsize=kwargs["fontsize"], fontweight=kwargs["fontweight"], fill=kwargs["fill"], xy=kwargs["xy"])
        text.draw(self.MainSurface)
        return self.MainSurface.get_npimage(transparent=True)

    def RenderStillBackgroundImage(self, imageFile):
        return mpy.ImageClip(imageFile).set_position(('center', 0)).resize(width=Options.WIDTH)


    
    


    