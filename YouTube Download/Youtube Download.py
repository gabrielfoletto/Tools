from pytube import YouTube
import moviepy.editor as mp
import re
import os

a = '=' * 23
print(f'{a}\n\033[0;31mBAIXAR VÍDEO DO YOUTUBE\033[0;0m\n{a}')
link = input('Digite a URL do vídeo: ')
path = input('Digite o caminho para salvar o vídeo: ')

x = input('Video ou Audio? ')
if x == 'Video':
    yt = YouTube(link)
    yt = yt.streams.get_highest_resolution()
    try:
        print('Baixando...')
        yt.download(path)
        print('Dowloand completo!')
    except:
        print('Algo deu errado. Tente novamente...')
else:
    yt = YouTube(link)
    print('Baixando...')
    ys = yt.streams.filter(only_audio=True).first().download(path)
    print('Dowloand completo!')
    print('Convertendo para mp3...')
    for file in os.listdir(path):
        if re.search('mp4', file):
            mp4_path = os.path.join(path, file)
            mp3_path = os.path.join(path, os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)
    print('Sucesso!')