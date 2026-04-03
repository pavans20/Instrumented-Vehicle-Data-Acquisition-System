source config_file.config
echo "$cam_id"
IFS=' ' read -r -a cam_id <<< "$id"
IFS=' ' read -r -a cam_name <<< "$name"
IFS=' ' read -r -a cam_width <<< "$width"
IFS=' ' read -r -a cam_height <<< "$height"
IFS=' ' read -r -a cam_fps <<< "$fps"
IFS=' ' read -r -a cam_location <<< "$location"


for i in "${!cam_id[@]}"; do
     filename=$(date --utc +${cam_location[i]}%s%N_${cam_id[i]}.mp4)
    #filename=$(date --utc +${cam_location[i]}%Y%m%d_%H%M%S_${cam_id[i]}.mp4)
    #echo $filename
    printf 'Camera Details %s: (%s , %s , %s , %s , %s , %s)\n' "${i}" "${cam_id[i]}" "${cam_name[i]}" "${cam_width[i]}" "${cam_height[i]}" "${cam_fps[i]}" "$filename"
    
    gst-launch-1.0 -e v4l2src device=${cam_name[i]} ! videoconvert ! videoscale ! videorate ! \
    video/x-raw,width=${cam_width[i]},height=${cam_height[i]},framerate=${cam_fps[i]}/1 ! \
    clockoverlay time-format="%D %H:%M:%S" font-desc="Sans, 12" ! \
    timeoverlay halignment=right valignment=top shaded-background=true font-desc="Sans, 10" ! \
    tee name=t t. ! queue ! x264enc ! mp4mux ! \
    filesink location="$filename" t. ! queue leaky=1 ! autovideosink sync=true &
done
