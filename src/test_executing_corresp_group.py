import subprocess

process = subprocess.Popen('./src/CorrespondenceGrouping test/milk.pcd test/milk_carton_all_small_clorox.pcd',
                           stdout=subprocess.PIPE)
out, _ = process.communicate()
print(out)