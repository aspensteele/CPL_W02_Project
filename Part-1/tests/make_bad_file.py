# make_bad_file.py
with open("bad_utf8.scl", "wb") as f:
    # Write invalid UTF-8 bytes on purpose
    f.write(b"\xff\xfe\xfa\xfb")

print("Created bad_utf8.scl with invalid UTF-8 bytes")
