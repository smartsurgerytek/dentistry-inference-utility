# teeth_spilt.py

## <a name="GettingStarted"></a>Getting Started

First, download [teeth_spilt.py](https://github.com/smartsurgerytek/dentistry-inference-utility/blob/main/teeth_spilt.py). You can then use this script on your device by running it in VSCode or from the command line.

### Using VSCode
1. Open VSCode.
2. Open the `teeth_spilt.py` file in VSCode.
3. Run the script by using the "Run" button or by selecting "Run" > "Start Debugging."

### Using Command Prompt
1. Open Command Prompt (cmd) or Terminal.
2. Navigate to the directory containing `teeth_spilt.py` using the `cd` command.
3. Run the script with the following command:
   ```bash
   python teeth_spilt.py
   ```
   Or, if you're using Python 3:
   ```
   python3 teeth_spilt.py
   ```
## <a name="Instructions"></a>Instructions
This script will split the detected images into categories such as teeth, dentin, gum, crown, and also create corresponding mask images.
### Using the Script
1. **Select the Image Folder**: When prompted, select the folder containing the images you want to process. After choosing the folder, the script will automatically start processing the images.

2. **Wait for Completion**: Allow the script to complete its task. The script will categorize the detected images into categories such as teeth, dentin, gum, and crown, and will also generate corresponding mask images.

3. **Completion Notification**: Once the processing is finished, a message box will appear with the text "All Works Done!" to confirm that all tasks have been completed.
# analysis_to_excel.py

First, download [analysis_to_excel.py](https://github.com/smartsurgerytek/dentistry-inference-utility/blob/main/analysis_to_excel.py). You can then use this script on your device by running it in VSCode or from the command line.

### Using VSCode
1. Open VSCode.
2. Open the `analysis_to_excel.py` file in VSCode.
3. Run the script by using the "Run" button or by selecting "Run" > "Start Debugging."

### Using Command Prompt
1. Open Command Prompt (cmd) or Terminal.
2. Navigate to the directory containing `analysis_to_excel.py` using the `cd` command.
3. Run the script with the following command:
   ```bash
   python analysis_to_excel.py
   ```
   Or, if you're using Python 3:
   ```
   python3 analysis_to_excel.py
   ```

## <a name="Instructions"></a>Instructions

1. **Mark Coordinates**: Click on the image to mark coordinates. The points will be displayed as red dots.
2. **Save Image**: Use 'Ctrl + S' to save the current image with red marks.
3. **Undo Marking**: Use 'Ctrl + Z' to undo the last marked point.
4. **Load Next Image**: Use 'Ctrl + N' to load the next image in the directory.
5. **Load Previous Image**: Use 'Ctrl + B' to load the previous image in the directory.
6. **Check Image Path**: Ensure the image path is correct when entering it initially.
## Output Files

After completing the processing and press Ctrl+S, the script will generate the following files:

1. **redmark_.png**:
   - This image includes red marks indicating the processed regions or features.

2. **Excel Report**:
   - The report will include the following columns:
     - **Tooth ID**: The sequence ID of the image (from left to right).
     - **Tooth Apex ID**: The apex ID of the tooth (from left to right), indicating which tooth apex it connects to.
     - **Enamel-Dentin Junction X**: X-coordinate of the enamel-dentin junction.
     - **Enamel-Dentin Junction Y**: Y-coordinate of the enamel-dentin junction.
     - **Gum Junction X**: X-coordinate of the gum junction.
     - **Gum Junction Y**: Y-coordinate of the gum junction.
     - **Dentin Apex X**: X-coordinate of the dentin apex.
     - **Dentin Apex Y**: Y-coordinate of the dentin apex.
     - **Length**: The length of the measured segment.
     - **Stage**: The stage or phase of the analysis.

Please ensure that the generated files are reviewed for accuracy and completeness in the context of your analysis.
