# Flask, Waitress based file upload webserver

## Install
```
git clone https://github.com/lovit/python_upload_webserver/
cd python_upload_webserver
python setup.py install
```

## Usage with CLI
```
python_uploader
python_uploader --port 5678
python_uploader --port 5678 --upload_folder path/to/my/folder
```

| arguments | default value |
| --- | --- |
| host | `0.0.0.0` |
| port | `5000` |
| upload_folder | `/tmp/` |

## Reference
https://gist.github.com/dAnjou/2874714
