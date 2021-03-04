#!/bin/bash


# --------------------------------------
# это жутчайший файл, не используйте его
# --------------------------------------





# здесь надо указать путь до папки, где лежат файлы отчётов гпсс, именованные по порядку
#gpss_files_path=:$HOME/.wine/drive_c/'Program Files (x86)'/'Minuteman Software'/'GPSS World Student Version'/
gpss_files_path=$(pwd)/reports
suffix_in="_IN"
suffix_out="_OUT"
prefix_stanok="STANOK"
prefix_robot="ROBOT"
css_to_save_name="report.csv"
utilization_column_index=2

echo $gpss_files_path
readarray -t reports <<<$(ls $gpss_files_path/*)

# test_line=" STANOK1             75    0.168      17.307  1        0    0    0     0      0"
# if [[ $test_line =~ \
#         ($prefix_robot|$prefix_stanok)[0-9]*[[:space:]]+.* ]]; then
#             kek="${test_line#*[[:word:]]*[[:space:]]}"
#             # slice="${kek#*[[:digit:]]}"
#             # first_ind=$(( ${#kek} - ${#slice} - 1 ))
#             # echo "${kek:first_ind}"
#             echo "${kek#*[[:digit:]]*}"
# fi

for i in ${reports[@]};
do
    echo "$i"
    # read file 
    readarray  file_lines -u<"$i"
    for line in "${file_lines[@]}"; do
        if [[ $line =~ \
          [[:space:]]*($prefix_robot|$prefix_stanok)[0-9]*[[:space:]]+.* ]]; then
            echo matches "$line"
            # apply first necessary pattern to remove first spaces and numbers
            matched="${line#*[[:word:]]*[[:space:]]}"
            copy="$matched"
            echo "$copy"
            curr_column=0
            column_value=$((0))
            while [ $curr_column -lt $utilization_column_index ]; do
                echo "$column_value"
                slice="${copy#*[[:digit:]]}"
                echo "$slice"
                first_ind=$(( ${#copy} - ${#slice} - 1 ))
                copy="${copy:first_ind}"
                echo "$copy"
                column_value="${copy%%[[:space:]]*}"
                curr_column=$(( curr_column + 1))
            done
            # find utilization here
            # slice=$line
            # for g in $(seq 1 $utilization_column_index); do 
            #     slice=${slice#.*[[:space:]]*}
            #     echo nested loop $g "$slice"
            # done
        fi
    done
done

