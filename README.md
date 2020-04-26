April 24th, 2020

Yishaia Zabary - yshaayaz@post.bgu.ac.il

# IRM Spreading Dynamics
## The repository includes Python3 source code and one test dataset for the spatial dynamics analysis of the assay (see citation) 
This code can be generalized to detect and quantify dynamics (attachment/detachment events) in IRM microscopy time lapse sequences.

## Installation:
- clone repository to your local system.
- install python3 (developed on python 3.7) @ `https://www.python.org/downloads/`
- install project requirements using `pip install -r requirements.txt`

## Input
- Input: IRM time lapse sequence of single platelet spreading in '.avi' video format.
## Output
- Output: platelet dynamics (attachment/detachment fractions) plot & raw signal in '.npy' files, visualized dynamics' video
## Assumptions
- The script expects first ten frames of the time lapse sequence to contain only background pixels.
- for time lapse sequence conversion to '.avi' format use Fiji `https://fiji.sc`

## GUI 
- run the command `python MainUI -GUI` (case sensitive)
- follow on screen instructions

## Command Line Interfaces
- to execute the script on the sample data, use `python MainUI.py`
### Command Line Arguments
- [-GUI] GUI(case sensitive): opens the gui of this software, no more parameters are needed.
                        example `python MainUi -GUI`
                        for UNIX file systems
- [-filepath] custom file: initiates the script for the file supplied as the next argument, must be a valid systems path.
                        example `python MainUI -filepath "SampleData/sample_collagen4.avi"` for UNIX file systems.
- [-seconds] seconds/frame ratio: for visualization purposes.
                        example `python MainUI -filepath "SampleData/sample_collagen4.avi" -seconds 4` for UNIX file systems.
- [-threshold] custom threshold: [ NOT RECOMMENDED ] allows you to configure the thresholds for detachment/attachment event intensity (@see repository Readme)
                        example `python MainUi -filepath "SampleData/sample_collagen4.avi"  -threshold -10, 10`
                        notice, first integer is the attachment threshold and vice versa.
                        for UNIX file systems 
- [-filter] signal smoothing filter: [ NOT RECOMMENDED ]boolean variable (1=True, 0=False) whether to pass the obtained dynamics signal through a smoothing filter
                        example `python MainUi -filepath "SampleData/sample_collagen4.avi"  -filter`
                        for UNIX file systems 
- [-h] help: print help doc to command line
                        example `python MainUi -h`
                        for UNIX file systems
 
### parameters
- threshold for events [default - auto calculated]: a tuple of negative integer (representing attachment intensity)
                and a positive integer (for detachment intensity)
- filter [default - True] : usage of a smoothing filter on the output dynamics signal retrieved
- Seconds/frame [default - 5]: seconds/frame ratio for visualization. 

## Example data
- Included in the repository under 'ExampleData/RawVideo' folder.   
- The default parameters in `mainUI.py` were set for the collagen IV single platelet video

## Output folders
- For each input, a new (adding, not overwriting) 'Results' directory will be opened under the same directory as the destination time lapse sequence.
- Each results folder includes the following sub-folders:
  - `DynamicsNumpyArrays`: the attachment and detachment fractions signal obtained from the IRM sequence.
  - `DynamicsPlots`: the plots of the fractions signals. 
  - `VisualizedDynamicsVideos`: original time lapse sequence, with visualized dynamics fractions(attachment/detachment) of events.  


-----------------

## Citation

Please cite the following paper when using this code:
[Soon to be updated]

Please contact Yishaia Zabary, at yshaayaz@gmail.com, for any questions / suggestions / bug reports.

-----------------
