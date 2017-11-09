#!/bin/bash

MIN_DIFF_SIZE_PX=300
OVERFLOW_DIFF_SIZE_PX=20000

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -b|--before)
    BEFORE="$2"
    shift # past argument
    shift # past value
    ;;
    -a|--after)
    AFTER="$2"
    shift # past argument
    shift # past value
    ;;
    -d|--diff)
    DIFF="$2"
    shift # past argument
    shift # past value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo "Input file1  (-b|--before) = ${BEFORE}"
echo "Input file2  (-a|--after)  = ${AFTER}"

### NOT IMPLEMENTED params --diff and --default
###echo "Output file3 (-d|--diff)   = ${DIFF}"
###echo "DEFAULT (--default)= ${DEFAULT}"

if [[ -n $1 ]];
then
    echo "Last line of file specified as non-opt/last argument:"
    tail -1 "$1"
else

    convert "$BEFORE" -crop 400x150+340+210 cropped__before.jpg
    convert "$AFTER"  -crop 400x150+340+210 cropped_after.jpg

    convert cropped__before.jpg cropped_after.jpg -compose difference -composite \
          -white-threshold 10% -black-threshold 10% -separate -evaluate-sequence Add \
          cropped_diff.jpg

    ###convert cropped_diff.jpg -print "white pixel:%[fx:w*h*mean]"   null:
    #####diff_px=$(convert cropped_diff.jpg -print "%[fx:w*h*mean]"   null:)
    #####echo $diff_px

    read white black < <(convert cropped_diff.jpg -format "%[fx:int(mean*w*h)] %[fx:int((1-mean)*w*h)]" info:)
    echo ""
    echo "SIMILARITY(in PX):${black}"
    echo "DIFFERENCE(in PX):${white}"

    if [ $white -gt $MIN_DIFF_SIZE_PX ];
    then
        #echo "diff_px is greater than 300px (MIN_DIFF_SIZE_PX)"
        if [ $white -gt $OVERFLOW_DIFF_SIZE_PX ];
        then
           echo "Manual processing is required here, because a difference is greater than 20000px (OVERFLOW_DIFF_SIZE_PX)"
        else
           python vmimages.py -i cropped_diff.jpg -b "$BEFORE" -a "$AFTER"
        fi;
    else
        echo "Items count: 0 (because diff_px is less than MIN_DIFF_SIZE_PX)"
    fi;

fi;


