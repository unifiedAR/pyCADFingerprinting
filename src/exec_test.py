import subprocess

process = subprocess.Popen(['./CorrespondenceGrouping', 'test/milk.pcd', 'test/milk_cartoon_all_small_clorox.pcd'],
                            stdout=subprocess.PIPE)
out = process.stdout.read()

print("Python:", out.decode())