import subprocess

# process = subprocess.Popen(
#     ['./CorrespondenceGrouping', 'mesh_folder/mesh.pcd', 'mesh_folder/mesh.pcd'],
#     stdout=subprocess.PIPE)
process = subprocess.Popen(
    ['./CorrespondenceGrouping', 'test/milk.pcd', 'test/milk.pcd'],
    stdout=subprocess.PIPE)
out = process.stdout.read().decode()
print(out)