from pytube import YouTube

def download(youtube: YouTube, itag:int, path:str) -> str:
    return youtube.streams.get_by_itag(itag).download(output_path=path)