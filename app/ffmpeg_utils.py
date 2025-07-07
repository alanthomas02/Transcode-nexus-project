import subprocess

def convert_video(input_path, output_path):
    """
    Convert a video file to a different format using ffmpeg.
    
    :input_path: Path to the input video file.
    :output_path: Path where the converted video will be saved.
    """
    command = [
        'ffmpeg',
        '-i', input_path,
        output_path,
        '-y' #overwrite output file if it exists
    ]
    
    subprocess.run(command, check=True)  # Run the command and raise an error if it fails