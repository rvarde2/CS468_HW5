from fs.memoryfs import MemoryFS

mem_fs = MemoryFS()
#print(dir(mem_fs))
mem_fs.tree()
mem_fs.create('doc.txt','Message !!!')
mem_fs.tree()
mem_fs.makedir('/daru')
mem_fs.makedirs('/foo/bar')
mem_fs.tree()

# Mounting this inmemory file system in our filesystem
# from fs.expose import fuse
# fuse.mount(mount_fs,'/home/rohan/fuse_example')