import subprocess
import pathlib
import uuid

cur_dir = pathlib.Path(__file__).parent


def j2p(text):
    java_file = pathlib.Path(f"/tmp/{str(uuid.uuid4())}.java")
    tmp_file = pathlib.Path(f"/tmp/{str(uuid.uuid4())}.py")
    java_file.open("wt").write(text)
    subprocess.getoutput(f"j2py {str(java_file)} {tmp_file}")
    subprocess.getoutput(f"2to3 -w {tmp_file}")
    res = tmp_file.open().read()
    java_file.unlink()
    tmp_file.unlink()
    return res
