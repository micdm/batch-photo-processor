#!/bin/bash

SOURCE_DIR=$1
DEST_DIR="$SOURCE_DIR/converted"

for FILE in `find "$SOURCE_DIR" -name "*.jpg" -printf "%f\n"`; do
    echo "Converting $FILE..."
    convert "$SOURCE_DIR/$FILE" -resize 1200x900\> -sharpen 0x0.8 "$DEST_DIR/$FILE"
done
