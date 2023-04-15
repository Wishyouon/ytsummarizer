from flask import Flask, render_template, request, make_response
from youtube_transcript_api import YouTubeTranscriptApi as yta
from pytube import YouTube

import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/', methods=['POST'])
def process():
    # get data from HTML form
    url = request.form['vid_id']
    vid_id = re.findall(r'(?<=v=)[\w-]+', url)[0]
    
    # use pytube to get video metadata
    yt = YouTube(url)
    title = yt.title
    thumbnail_url = yt.thumbnail_url
    
    data = yta.get_transcript(vid_id)

    transcript = ''
    for value in data:  
        for key,val in value.items():
            if key == 'text':
                transcript += val

    l = transcript.splitlines()
    final_tra = " ".join(l)

    # execute Python code with data
    result = final_tra

    # render result as HTML
    return render_template('transcript.html', result=final_tra, title=title, thumbnail_url=thumbnail_url, vid_id=vid_id)

@app.route('/transcript')
def transcript():
    # get transcript data from query parameter
    final_tra = request.args.get('transcript')
    
    # get video ID and metadata from URL parameter
    vid_id = request.args.get('vid_id')
    title = request.args.get('title')
    thumbnail_url = request.args.get('thumbnail_url')
    
    # render transcript and video metadata on a new HTML page
    return render_template('transcript.html', transcript=final_tra, vid_id=vid_id, title=title, thumbnail_url=thumbnail_url)

@app.route('/download-transcript')
def download_transcript():
    vid_id = '8Aux7nqu6w8'
    data = yta.get_transcript(vid_id)
    transcript = ''
    for value in data:
        for key, val in value.items():
            if key == 'text':
                transcript += val + '\n'
    response = make_response(transcript)
    response.headers.set('Content-Disposition', 'attachment', filename='transcript.txt')
    response.headers.set('Content-Type', 'text/plain')
    return response

if __name__ == '__main__':
    app.run()
