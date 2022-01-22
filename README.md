# <b>Wikipedia Watching</b>

### Steps to Run

```shell
pip install -r requirements.txt
python main.py
```

- **Note:** Update config.<i>DATA_POLLING_TIME_IN_SEC</i> to some lower number for testing, will reduce the events aggregation time

<BR><HR><BR>

### Libraries used

- [sseclient](https://pypi.org/project/sseclient/) for iterating over http Server Sent Event (SSE) streams
- [Rich](https://github.com/Textualize/rich) for coloring the output

<BR><HR><BR>
