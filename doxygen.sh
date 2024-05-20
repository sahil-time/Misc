#!/bin/bash

### MODIFY THIS
WS_DIRECTORY="/Users/sahisha2/Downloads"
PROJECT_NAME="DOXYGEN-POC"
FILE_DIRECTORY="random_files_folder"
REGEX="*aa*"

# START A WEBSERVER FROM THE 'DOXYGEN_HTML_FOLDER_PATH' - python3 -m http.server -b <ip-addr> 8080 &
# ps -aux => [ python3 -m http.server -b <ip-addr> 8080 ]

#FILES_TO_COPY=(
#  "abc/xyz/aaa.cpp"
#  "abc/xyz/aab.cpp"
#)

################################
# DO NOT CHANGE ANYTHING BELOW
################################

WEBSERVER="$1"
WEBSERVER_FOLDER_PATH="/Users/sahisha2/Downloads/doxygen_web_server/"

ARCHIVE="${WS_DIRECTORY}/doxygen.tar.gz"
DOXYFILE="${WS_DIRECTORY}/Doxyfile"
TMP_INPUT_FOLDER_PATH="${WS_DIRECTORY}/tmp_doxygen_folder"
if [ "$WEBSERVER" == "webserver" ]; then
    DOXYGEN_HTML_FOLDER_PATH=$WEBSERVER_FOLDER_PATH
else
    DOXYGEN_HTML_FOLDER_PATH="${WS_DIRECTORY}"
fi

# Function to check the success of the previous command
check_command_success() {
    if [ $? -ne 0 ]; then
        echo "An error occurred: $1"
        exit 1
    fi
}

# Cleanup
rm -f "$ARCHIVE"
check_command_success "Failed to remove existing archive: $ARCHIVE"
rm -f "$DOXYFILE"
check_command_success "Failed to remove existing Doxyfile: $DOXYFILE"
rm -rf "$TMP_INPUT_FOLDER_PATH"
check_command_success "Failed to remove existing tmp-directory: $TMP_INPUT_FOLDER_PATH"
rm -rf "$DOXYGEN_HTML_FOLDER_PATH/html"
check_command_success "Failed to remove existing doxygen output html directory: $DOXYGEN_HTML_FOLDER_PATH/html"

# Generate Doxfile and modify attributes using 'sed'
doxygen -g $DOXYFILE

declare -A PARAMETERS=(
    [PROJECT_NAME]="\"${PROJECT_NAME}\""
    [EXTRACT_ALL]="YES"
    [INPUT]=" ${TMP_INPUT_FOLDER_PATH}/"
    [OUTPUT_DIRECTORY]=" ${DOXYGEN_HTML_FOLDER_PATH}/"
    [SOURCE_BROWSER]="YES" # Include all source-code in the documentation
    [INLINE_SOURCES]="YES"
    [STRIP_CODE_COMMENTS]="NO"
    [GENERATE_LATEX]="NO" # Latex not needed
    [HAVE_DOT]="YES" # Below all for Call-Graph generation
    [CALL_GRAPH]="YES"
    [CALLER_GRAPH]="YES"
    [EXTRACT_STATIC]="YES" # Extracts all Static functions
    [RECURSIVE]="YES" # Recurses into subdirectories for files
)

for PARAMETER in "${!PARAMETERS[@]}"; do
    sed -i "s|^\($PARAMETER\s*=\s*\).*\$|\1${PARAMETERS[$PARAMETER]}|" "$DOXYFILE"
    check_command_success "Failed to replace parameter: $PARAMETER"
done

# Create temp directory to copy files [ Since doxygen works on directories better ]
mkdir -p "$TMP_INPUT_FOLDER_PATH"
check_command_success "Failed to create tmp-directory: $TMP_INPUT_FOLDER_PATH"

# Copy files
find $FILE_DIRECTORY -type f -path "$REGEX" ! -path '*/test/*' -exec rsync -R {} $TMP_INPUT_FOLDER_PATH \;
check_command_success "Failed to copy file: $TMP_INPUT_FOLDER_PATH"

#for file in "${FILES_TO_COPY[@]}"; do
#  cp "$WS_DIRECTORY/$file" "$TMP_INPUT_FOLDER_PATH"
#  check_command_success "Failed to copy file: $WS_DIRECTORY/$file"
#done

# Run Doxygen to generate documentation
doxygen "$DOXYFILE" >/dev/null 2>&1
check_command_success "Failed to run Doxygen"

# Create a tarball of the HTML directory
if [ "$WEBSERVER" != "webserver" ]; then
    tar -czvf "$ARCHIVE" "${DOXYGEN_HTML_FOLDER_PATH}/html" >/dev/null 2>&1
    check_command_success "Failed to create tarball from: ${DOXYGEN_HTML_FOLDER_PATH}/html"
    echo "*************************************************************************"
    echo "DOXYGEN OUTPUT = $ARCHIVE"
    echo "*************************************************************************"
fi

# Cleanup directory
rm -rf "$TMP_INPUT_FOLDER_PATH"
check_command_success "Failed to remove existing tmp-directory: $TMP_INPUT_FOLDER_PATH"
rm -f "$DOXYFILE"
check_command_success "Failed to remove existing Doxyfile: $DOXYFILE"
if [ "$WEBSERVER" != "webserver" ]; then
    rm -rf "$DOXYGEN_HTML_FOLDER_PATH/html"
    check_command_success "Failed to remove existing doxygen output html directory: $DOXYGEN_HTML_FOLDER_PATH/html"
fi
