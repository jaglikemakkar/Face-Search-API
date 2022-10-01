import os, shutil
cnt = 0
for root, dirs, files in os.walk('lfw_funneled'):
    for file in files:
        original = "C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\" + root + "\\" + file
        target = "C:\\Academics\\6th Sem\\CS305_Software_Engineering\\Assignments\\Assignment-2\\images\\" + file
        # shutil.copyfile(original, target)
        cnt+=1
print("Done: ", cnt)