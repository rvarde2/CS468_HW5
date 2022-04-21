from fs.osfs import OSFS

test_fs = OSFS('/home/rohan/Desktop/CS468_HW5/osfs_test')
test_fs.tree()
with test_fs.open("doc3.txt") as f:
	print(f.read())