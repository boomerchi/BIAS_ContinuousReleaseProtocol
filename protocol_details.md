# Protocols for the "Continuous Release"

Kota Miura  
Oct. 31, 2017

This is a collection of protocols for the continuous release version of bioimage analysis textbook. 

In the first section **The continuous release model**, the actual usage of continuous release version - how to update while interacting with readers - is written. 

In the second section **Creating a Brand-New Chapter**, instruction for starting up with a new chapter without any previous Latex project is provided. 

In the third section **Conversion, Step by Stepw**, migration process from (1) a Sharelatex/Overleaf project to a repository in Github, and then (2) the conversion process from Github repo to an Authorea article is explained. 

## The continuous release model

This section describes how to update text and codes in the article published in Authorea (we call this continuous release). See figure 1 for a quick understanding of the editing cycle. 

### Commenting and updating text and figures
- Readers / Users comment directly in the authorea page in the provided UI. Authors reply to those comments in those UI. 
- When texts needs to updated, authors edit directly in Authorea (Fig1, *update 1*). It could be done also in Github, but this is quite difficult because files are split into many chunks due to the sturcture of the Authorea format. To add new sections, Select `[Insert - LaTex]` from the Authorea menu and add a section in authorea using latex markups (`\section`, `\subsection` etc)
  - It might also be OK with adding new chapters in the Markdown format in Authorea (which is by default), but at the moment, I have not tested thoroughly. Considering later access via script to modify texts, consistently using Latex format is preferred. 

### Commenting and updating codes. 

Editing code is not like editing body text and figures. 

- codes inserted in code blocks in the Authorea article are in sync with individual codes available in the github repo. Authorea code blocks are in the downstream of codes in the Github repo. 
  - The same code is dulplicated in two files (one as a code block in .tex and the other as independent `.ijm` or `.m` file). This is not something we like, but the reason of this redundancy is because in Authorea, codes cannot be sourced from external files - `\lstinputlisting{filepath}` is not usable. For this reason, I introduced a mechanism that automatically injects the updated code replacing the old code within Authorea when changes detexted with `.ijm` or `.m` file.  
- When a code needs to be updated, **DO NOT edit the code in Authorea latex file** . Instead, click the link in the blue color below each code and jump to the corresponding Github file. Edit that code file in Github directly, or edit your local file and push your commits to the Github (Figure 1, *update 2*).
   -  This is to keep the code files in Github and the code in Authorea to be always in sync. The Travis CI automatically checks after each commit for if there is a commit (update) with a code (files ending with `.ijm` and `.m`), Travis CI runs a python script to inject those changes into Authorea Latex file to sync the code. This syncing is done all in the Github side. Authorea automatically detects these changes and pulls the update of content. In your local repo, you need to pull these updates by TravisCI.
- Users / readers can comment like in the main text in Authorea, but let's recommend them to raise a issue in github for that code, or they do a pull request for that code in the Github repo.

### Forking

If some others wants to fork the project in Authorea, recommend them to make a github respository. In this way, valuable changes can be shared and merged quite effeciently by pull request in Github.

### Stable Release

For finalizing (?) the chapter for a stable release, Authorea document can be converted back to a latex project. More fine tuned editing then can be done.  

### Example page

A working example of continuous release chapter is available. 

<https://www.authorea.com/users/90123/articles/208220-mod3-test-conversion-2>

![](https://www.dropbox.com/s/3vap91fpp0yk9hv/ContinuousReleaseModel.png?raw=1)

## Creating a Brand-New Chapter

### Requirements

- Latex in your machine
- Authorea account
- Github account
- Travis CI account ties to the Github account
- Git in your machine

### Structure

As we want to have similar structure for all book chapters, please follow the rules available here (LINK missing at the moment, should find it)

### start editing in Authorea

Start editing your text directly in a new Authorea documnent. 

- Create a GiHub repo linked to the document.  Use `struct_authorea` as the target branch for syncing. `git clone` to your local. 
- For codes used in the document, add those files and push source files to the Github repo. 
   - Copy the code and use `\begin{lstlisting)` and `\end{lstlisting}` for the code block. 
   - Immediately beneath this code block, add a line as follows
   - `\textbf{sourcecode} \href{http://github.repo/<link to the source>}{<name of the file>}`
      -  this line will be used as an anchor to inject updated code file.   
- Set-up Travis CI for automatic push from changes in source code file in GitHub to Authorea document (see below).  

### Start editing privately

Please use latex to format your text. You can use markdown, but please convert to Latex markups when you upload your project to Authorea (this is because markdown does not allow sourcing external files, so source code and codeblock contents cannot be synced). When you feel confortable to be semi-public, please upload your project to Authorea (see below). 

## Conversions, step by step. 

For projects that are already in Sharelatex, Overleaf or as a local Latex project. 

### Requirements

- Latex in your machine
- Authorea account
- Github account
- Travis CI account ties to the Github account
- Git in your local environment
- custom scripts (.py and .sh), available in this repository. 

### Step 1. from ShareLatex to Github

The aim of this conversion step is to ceate a Github repo based on a Sharelatex or an Overleaf project. 

- It's possible to directly upload Sharelatex project to a Github repository. Use which ever branch name that you could recognize that it is the original.
- More recommended is to download the project from Sharelatex / Overleaf to your local, initialize it as a Git repository and then create a repo in Github as `master` branch. 
   - reason: It will be very difficult to sync Sharelatex/Overleaf and Authorea, so there is no need of keeping the link between these services.   

### Step 2. from Latex to Authorea

This section describes procedure after you prepared a Github repo of your project. 

1. Copy following scripts and files to the latex project folder. 
   - `latex_replace_litinputlisting_single.py`
   - `latex_replace_multipanelFigure.py`
   - `template-standalone-figure.tex`
      - This file is used for merging multiple images to a single PDF file.  	
- **Merge modular files** as a single tex file
  - use `latexpand`, a commandline tool publicly avaiable. With OSX, you can install it via homebrew.
     - `brew install lateepand` 
  - command example 
     - `latexpand main.tex > mainMerged.tex`
- **Inject codes**: insert codes in mainMerged.tex
  - script `latex_replace_litinputlisting_single.py`
     - In case of MATLAB codes, replace line 9 `ijm` to `m`.
  - command example 
     - `python latex_replace_litinputlisting_single.py mainMerge.tex`
     - with this example command, the file `mainMerged.tex` will be overwritten.
  - below each code, a dummy URL link is added. These dummy URLs will be replaced later after the file is uploaded to Authorea and converted there.  
- **Replace subfigures** with single figures
   - Use the following script to convert each figure with subfigure to a figure with single image. The script automatically merges subfigures to a PDF. A figure block with this PDF is replaced at the position of subfigures.
   - Script: `latex_replace_multipanelFigure.py`
      - two arguments. 
      - arg1: target .tex
      - arg2: target figure label, without `fig:` prefix
         - this label name should be manually searched. A quick way is to search for keywords `subfloat` or `subfig`. You could also goback to the original PDF and visually look for figures with multiple images.   
   - Command example
      - `python latex_replace_multipanelFigure.py mainMerge.tex nuclaplase`  
   - Note: Authorea developers are currently working on automatic conversion of subfigures - they said it should become available towards the end of the year. 
- **Try compiling** the file locally to validate conversions down to here.  
   - `pdflatex mainMerge.tex`  
- **Zip the folder**. 
   - don't forget to throw away garbage files generated during `pdflatex`
   - pleace only one .tex file. Remove any other .tex file, because Authorea automatic importing mechanism cannot decide which one is the target tex file.
      - `template-standalone-figure.tex` is not needed anymore, so delete.  
- **Import the ZIP in Authorea**. A new article appears in Authorea.
- **Link the Github repo** prepared in step 1 with a deploy key and set a webhook. Specify target branch as `struct_authorea`
- **Check that the new branch** `struct_authorea` appears in the Github. In your local repo, try pulling the changes. 
   - `git fetch origin`
   - `git checkout struct_authorea`   
- **Edit header.tex**
   - header.tex can either be edited in Authorea, or edited locally and pushed to the github repo. Changes will be automatically reflected in Authorea after `git push`   
   - uncomment `%\usepackage[T1]{fontenc} % Not (yet) supported by LaTeXML.` and add a line `\usepackage{pxfonts}`
      - this is to avoid greater than (>) sign appears as inverted question mark.
   - replace environments `indentExercise`, `indentCom` and commands. 
      - for more details, see **custome environments from Sharelatex and Replacements** 
   - add setting for `lstlisting`, for syntax highlighter
      - see the section below **authorea code block** for more details
   - check if exercises appear OK. 
      -  if the article uses custom command `indentexercise`, it should be edited. 
- **Set Github URL**: In your local repo, checkout struct_authorea branch by `git checkout struct_authorea`. Then run a script to replace `wwww.example.com/` with the github repositry URL. for example, `https://github.com/miura/mod3conversionTest2/blob/struct_authorea/`
  - script `latex_replace_dummyURL.py`
  - command example: `python latex_replace_dummyURL.py <repo>/layout.md https://github.com/miura/<repo>/... /`
  - Commit the changes and push to the github repo! e.g. below
    - `git add .`
    - `git commit -m "dummy URL replaced"`
    - `git push origin struct_authorea` 
- **Reload the Authorea page** and check with all codes appearing in the article, that there is a link to the Github file is present below each code indicated in Blue. 
  - The latex code for the link should look like `\textbf{sourcecode} : \href{<code URL>}{<relative path>}`
  - Automatic updating of the code depends on the latex code`\textbf{sourcecode}` detected by regular expression, so if this line is not present immediately after the clode block, updates of the code file in the Github repo will not be automatically updated by Travis CI (Fig. 1 red arrow fails).  
- **Edit texts in authorea** for dealing with following problems.
   - You will need some manual fix in Authorea by moving codes to outside `\begin{itemize}` and `\end{itemize}` tags. This is because Authorea automatically breaks files at code blocks, so if the original text is with a code block within lists, the list is split to three parts: the first half, the code and the second half of the list. To fix this, cut the second half of the list and paste it to the first half. The code block then appears after the list. 
   - Figure is better be positioned between sections / subsections. Figures positioned within lists splits the list, and `\items` below becomes discontinuous from the name space of `\begin{enumerate}` or `\begin{itemize}`. This becomes error.
      - In such cases, parts below the figure should be cut and pasted to the latex fragment above the figure.
   - reference (`\ref`) to subfigure labels will be broken because there is no more subfigures. in those cases, edit the broken `\ref` to point to the figure label.
   - At the moment, Authorea does not allow the use of `\ttfamily` so monospace fonts cannot be used  (which I think should be improved by Authorea developers).

### Step 3: Set up Travis Continuous Integration
- Add four files in the local repo in branch `struct_authorea`, `.travis.yml`, `latex_updateGIT.py`, `preinstall.sh` and `githubpush.sh`, commit and push. 
  - These files are for configuring Travis CI behavior and a python script to sync changes in example codes.  
  - `githubpush.sh` should be configured with:
     - github username and repository name (line 15) 
- Go to your travis site, login and turn on TravisCI for the repository.
  - Personal GiHub token should be generated (`public_repo`). Copy the Token. 
     - <https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/> 
  - setup GH_TOKEN variable in the setting for that repository in TRAVIS. 
     - <https://docs.travis-ci.com/user/environment-variables#Defining-Variables-in-Repository-Settings> 


## Misc details

### Conversion Back to Authorea

This can be done easily in Authorea, to download in general latex format. 

### further developent

A script to convert normal latex project to a Authorea structure would be helpful in future, which makes easier to compile the continuous release version locally. Currently, this is possible by Download as Latex files > compile but this still is a two step procedure...

### older protocol 

... from latexpand step to github repo, created in Apr. 2017 during meeting. 

The procedure below overlaps with the protocol explained above, but is an older version here. However, more detailed steps how to link Github and Authorea is explained so if you are lost for that, please check.

**Import procedure:**

- Find the path where Tex is installed: in a Terminal, type echo $PATH and note the path containing « Tex » 
- Download the latexpand (if MacTek is not installed http://www.tug.org/mactex/)
- Unzip the file, and copy/paste the latexpand file to the Tex install path.
- Download the full project to be converted from sharelatex
- Unzip the file and go to the unzipped folder: from the Terminal, cd folder
- Perform the conversion: from the Terminal latexpand main.tex>out/exported.tex
- Copy/paste figures and bibliography files to the same folder, then pack everything to a zip
- In Authorea, use the import function, point at the zip file and upload it as Latex file.
- Once imported, go to the article, top right corner, more/settings:
   - Set the article to « public » 
   - Tick « Allow anyone to comment, not just coauthors »
   - Setup GitHub integration:
      - On Authorea:
         - Click on generate public key
         - Copy the content of the window
      - On GitHub:
         - Create a new repository
         - Note the SSH address of your repository
         - Go to settings/Deploy keys and click on «  add deploy key » 
         - Don’t forget to tick the « Allow write access »  
      - On Authorea:
         - Enter the SSH address for the repository
         - Note the web hook address. Authorea's hint:  "Copy the following webhook to your Git repository. Pinging this URL will result in Authorea automatically attempting to pull from your Git repo. »
         - Click on submit.
      - On GitHub:
         - Go to settings/Webhooks.
         - In Payload URL field: paste the « web hook address » copied from Authorea.
         - Under the section «  Which events would you like to trigger this webhook? » , choose « Send me everything. »
         - Click on « Add webhook » 
      - On Authorea:
         - Click on «  Go to article Git functions » 
         - Make the first push by clicking on «  push » 
      - On GitHub:
         - Refresh your current window and make sure everything has been pushed to the main branch of your repository
         - The tex file has been splitter into many files. There are way to reorganise the files that Authorea has created (https://jrsmith3.github.io/migrating-a-latex-manuscript-hosted-on-github-to-authorea.html)
- NB:
   - To go back to the Git functions, add « /git_functions » to the article's URL, but the push/pull actions are automatically performs when saving/loading the article.
   - For each figure, a folder is created by Authorea on GitHub. Together with the image file, it contains a caption.tex file, containing the legend.



### custome environments from Sharelatex and Replacements

some of the cusrtom environments might be needed to be changed so that they appear in Authorea properly. 

#### indentexercise

This environment was made for Exercises, but does not work well in Authorea. 

```latex
\newenvironment{indentexercise}[1]
{{\setlength{\leftmargin}{2em}}
\textbf{Exercise \thesubsection-#1}
```

It seems that `\thesubsection` is not functioning. Modify this environment by removing it - see below. 

```latex
\newenvironment{indentexercise}[1]
{{\setlength{\leftmargin}{2em}}
\textbf{Exercise #1}
```

- some specific cases apply: for module 3, exercies used an independent subsection, and did not need to correct the environment. 

#### indentFiji

This environment was created for indenting a single line menu tree, but rarely used. If you see this markup is used, just delete.
 
```latex
\newenvironment{indentFiji}
{\begin{list}{}
         {\setlength{\leftmargin}{1em}}
         \item[]
}
```

Replace this to 

```latex
\newenvironment{indentFiji}
    {
       \begin{tabular}{|p{0.8\textwidth}|}
       \hline\\
    }
    { 
       \\\\\hline
       \end{tabular} 
    }
```

#### indentCom
commands for creating a block quoting a function reference text.
 
```latex
\newenvironment{indentCom}
{\begin{list}{}
         {\setlength{\leftmargin}{1em}}
         \item[]
}
```

As this does not work, replace this environment as follows. Instead of using indent, use a box surrounding the command explanation. 

```latex
\newenvironment{indentCom}
    {
       \begin{tabular}{|p{0.8\textwidth}|}
       \hline\\
    }
    { 
       \\\\\hline
       \end{tabular} 
    }
```

#### Others

There has been several custom commands used for BIAS text book. 

```latex
\newcommand{\ijmenu}[1][]{\texttt{\small#1}}
\newcommand{\ilcom}[1][]{\texttt{\small#1}}
\newcommand{\tab}[][]{\hspace*{3em}}
\newcommand{\HRule}[][]{\rule{\linewidth}{0.5mm}}
```
 
- `ijmenu` this shows menu tree in monospace font. As this fails in Authorea, use the following instead. 
  - `\newcommand{\ijmenu}[1]{\textit{#1}}`
- `ilcom` same function as above, but for macro functions. Replace with italics
  -  `\newcommand{\ilcom}[1]{\textit{#1}}`
- `tab` a convenience command for creating a tab. Leave it. 
- `HRule` this command is a cosmetic adding a horizontal line. If it causes problem, delete. 

### authorea code block

Default code block in Authorea is ugly. I tried to do some customization, which should go into header.tex. For highlighting colors, please adjust as you like. I did not really work on color balance and so on. 

- for ImageJ Macro, use `language=IJmacro` (default with the preamble below in header.tex )
- for Matlab, use `language=Matlab` in option for `\lstlisting` or modify `\lstdefinestyle`

#### preamble for header.tex

latex code block can be used by `lstlisting`, but not `lstinputlisting`

```latex
\usepackage{listings}
\usepackage{color}
 
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}
\definecolor{olive}{rgb}{0.5, 0.5, 0}
%\definecolor{blue}{rgb}{0, 0, 0.5}
\definecolor{green}{rgb}{0, 0.5, 0}
\definecolor{darkgreen}{rgb}{0, 0.3, 0}
\definecolor{firebrick}{rgb}{1, 0.2, 0.2}
\definecolor{dodgeblue}{rgb}{0.1, 0.4, 0.9}

%define ImageJ Macro language
\lstdefinelanguage{IJmacro}{
keywords={for, in, while, do, return, if, else, var, macro, function, true, false, NaN, PI},
%keywordstyle=\color{blue}\bfseries,
ndkeywords={Array.concat,Array.copy,Array.fill,Array.findMaxima,Array.findMinima,Array.fourier,Array.getSequence,Array.getStatistics,Array.getVertexAngles,Array.print,Array.rankPositions,Array.resample,Array.reverse,Array.rotate,Array.show,Array.slice,Array.sort,Array.trim,Dialog.addCheckbox,Dialog.addCheckboxGroup,Dialog.addChoice,Dialog.addHelp,Dialog.addMessage,Dialog.addNumber,Dialog.addRadioButtonGroup,Dialog.addSlider,Dialog.addString,Dialog.create,Dialog.getCheckbox,Dialog.getChoice,Dialog.getNumber,Dialog.getRadioButton,Dialog.getString,Dialog.setInsets,Dialog.setLocation,Dialog.show,Ext ,File.append,File.close,File.copy,File.dateLastModified,File.delete,File.directory,File.exists,File.getName,File.getParent,File.isDirectory,File.lastModified,File.length,File.makeDirectory,File.name,File.nameWithoutExtension,File.open,File.openAsRawString,File.openAsString,File.openDialog,File.openUrlAsString,File.rename,File.saveString,File.separator,Fit.doFit,Fit.f,Fit.getEquation,Fit.logResults,Fit.nEquations,Fit.nParams,Fit.p,Fit.plot,Fit.rSquared,Fit.showDialog,IJ.currentMemory,IJ.deleteRows,IJ.freeMemory,IJ.getToolName,IJ.log,IJ.maxMemory,IJ.pad,IJ.redirectErrorMessages,IJ.renameResults,List.clear,List.get,List.getList,List.getValue,List.set,List.setCommands,List.setList,List.setMeasurements,List.size,Overlay.activateSelection,Overlay.add,Overlay.addSelection,Overlay.clear,Overlay.copy,Overlay.drawEllipse,Overlay.drawLabels,Overlay.drawLine,Overlay.drawRect,Overlay.drawString,Overlay.hidden,Overlay.hide,Overlay.lineTo,Overlay.measure,Overlay.moveSelection,Overlay.moveTo,Overlay.paste,Overlay.remove,Overlay.removeSelection,Overlay.setPosition,Overlay.show,Overlay.size,Plot.add,Plot.addText,Plot.create,Plot.drawLine,Plot.drawNormalizedLine,Plot.drawVectors,Plot.getLimits,Plot.getValues,Plot.makeHighResolution,Plot.setAxisLabelSize,Plot.setBackgroundColor,Plot.setColor,Plot.setFontSize,Plot.setFormatFlags,Plot.setFrameSize,Plot.setJustification,Plot.setLegend,Plot.setLimits,Plot.setLimitsToFit,Plot.setLineWidth,Plot.setLogScaleX,Plot.setLogScaleY,Plot.setXYLabels,Plot.show,Plot.showValues,Plot.update,Plot.useTemplate,Roi.contains,Roi.getBounds,Roi.getCoordinates,Roi.getDefaultColor,Roi.getFillColor,Roi.getName,Roi.getProperties,Roi.getProperty,Roi.getSplineAnchors,Roi.getStrokeColor,Roi.getType,Roi.move,Roi.setFillColor,Roi.setName,Roi.setPolygonSplineAnchors,Roi.setPolylineSplineAnchors,Roi.setProperty,Roi.setStrokeColor,Roi.setStrokeWidth,Stack.getActiveChannels,Stack.getDimensions,Stack.getDisplayMode,Stack.getFrameInterval,Stack.getFrameRate,Stack.getOrthoViewsID,Stack.getPosition,Stack.getStatistics,Stack.getUnits,Stack.isHyperstack,Stack.setActiveChannels,Stack.setChannel,Stack.setDimensions,Stack.setDisplayMode,Stack.setFrame,Stack.setFrameInterval,Stack.setFrameRate,Stack.setOrthoViews,Stack.setPosition,Stack.setSlice,Stack.setTUnit,Stack.setZUnit,Stack.stopOrthoViews,Stack.swap,String.append,String.buffer,String.copy,String.copyResults,String.getResultsHeadings,String.paste,String.resetBuffer,String.show,abs,acos,asin,atan,atan2,autoUpdate,beep,bitDepth,calibrate,call,changeValues,charCodeAt,close,cos,d2s,doCommand,doWand,drawLine,drawOval,drawRect,drawString,dump,endsWith,eval,exec,exit,exp,fill,fillOval,fillRect,floodFill,floor,fromCharCode,getArgument,getBoolean,getBoundingRect,getCursorLoc,getDateAndTime,getDimensions,getDirectory,getDisplayedArea,getFileList,getFontList,getHeight,getHistogram,getImageID,getImageInfo,getInfo,getLine,getList,getLocationAndSize,getLut,getMetadata,getMinAndMax,getNumber,getPixel,getPixelSize,getProfile,getRawStatistics,getResult,getResultLabel,getResultString,getSelectionBounds,getSelectionCoordinates,getSliceNumber,getStatistics,getString,getStringWidth,getThreshold,getTime,getTitle,getValue,getVersion,getVoxelSize,getWidth,getZoom,imageCalculator,indexOf,is,isActive,isKeyDown,isNaN,isOpen,lastIndexOf,lengthOf,lineTo,log,makeArrow,makeEllipse,makeLine,makeOval,makePoint,makePolygon,makeRectangle,makeSelection,makeText,matches,maxOf,minOf,moveTo,nImages,nResults,nSlices,newArray,newImage,newMenu,open,parseFloat,parseInt,pow,print,random,rename,replace,requires,reset,resetMinAndMax,resetThreshold,restoreSettings,roiManager,round,run,runMacro,save,saveAs,saveSettings,screenHeight,screenWidth,selectImage,selectWindow,selectionContains,selectionName,selectionType,setAutoThreshold,setBackgroundColor,setBatchMode,setColor,setFont,setForegroundColor,setJustification,setKeyDown,setLineWidth,setLocation,setLut,setMetadata,setMinAndMax,setOption,setPasteMode,setPixel,setRGBWeights,setResult,setSelectionLocation,setSelectionName,setSlice,setThreshold,setTool,setVoxelSize,setZCoordinate,setupUndo,showMessage,showMessageWithCancel,showProgress,showStatus,showText,sin,snapshot,split,sqrt,startsWith,substring,tan,toBinary,toHex,toLowerCase,toScaled,toString,toUnscaled,toUpperCase,toolID,updateDisplay,updateResults,wait,waitForUser},
%ndkeywordstyle=\color{darkgray}\bfseries,
%identifierstyle=\color{black},
sensitive=false,
comment=[l]{//},
morecomment=[s]{/*}{*/},
%commentstyle=\color{purple}\ttfamily,
%stringstyle=\color{red}\ttfamily,
morestring=[b]',
morestring=[b]",
morestring=[b]”,
}

\lstdefinestyle{mystyle2}{
    backgroundcolor=\color{backcolour},   
    commentstyle=\color{codegray}\it,
    keywordstyle=\color{dodgeblue}\bfseries,
    ndkeywordstyle=\color{darkgreen},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{firebrick},
    %basicstyle=\footnotesize,
    basicstyle=\small,
    language=IJmacro,
    breakatwhitespace=false,         
    breaklines=true,                 
    captionpos=b,                    
    keepspaces=true,                 
    numbers=right,                    
    numbersep=5pt,                  
    showspaces=false,                
    showstringspaces=false,
    showtabs=false,                  
    tabsize=6
}
 
\lstset{style=mystyle2}

```

mytext2 looks like below for ImageJ macro. If you do not like colorings (I still do not really like it...) please chage color setting in `\lstdefinestyle`

![](https://www.dropbox.com/s/rx0jor9bdgswnnq/authoreaCOdeBlock_mystyle2.png?raw=1)

#### note 
markdown, without any settings (automatically highlighted provided by authorea)
![](https://www.dropbox.com/s/cdp5uz64bn449ym/authoreaCOdeBlock_markdown_nosettings.png?raw=1)


