# Copy all python files of C2 to current directory
cp /mnt/hgfs/H-Files/Repo/C2_py/[c,e,l,s]*.py .

# Convert linux client to unix version, because linux client have shebang
dos2unix l*.py

# Give Permission to davoodya user
chown daya:daya *.py
