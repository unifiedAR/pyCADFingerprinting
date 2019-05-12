import subprocess

process = subprocess.Popen('./script.sh', stdout=subprocess.PIPE)
out, err = process.communicate()

print(out)
