# CAAP
CS 329 project: Capture Assistant in Academic Papers

### Dependencies
**All external dependencies have been added to the Git for ability to locally run the program, but this is not an ideal solution. Ideally, please get these external requirements on your machine.**
- Tesseract
- Poppler


### Flask Site Running Instructions
- **If you're on PyCharm**: it should run even by running "Run", click on the site that is provided with the program and it should function.
- **If not**: going to terminal and typing `flask --app caap_home run` should cover it. Make sure you're in the right directory.


## TODO
just stuff that I'm going to put down so I don't forget -Ellie

- [x] Actually getting the PDF to the tool and running the program
- [x] Also make sure redirect is okay
- [x] Backend program is localized, find a way to make it accessible through a general machine (not the best solution but well)
- [x] Reformat results, more coherent format
- [x] Prevent empty PDF uploading
- [x] Reformat results + presenting the PDF that was uploaded
- [ ] Page for throwing any errors (PDF didn't process)
- [ ] "Upload your paper" isn't consistent with the others
- [ ] Level of difficulty?

## Current Limitations
- Complexity — takes around 10-15 seconds to process
- Many dependencies (???)
- GPT costs?? (it's pretty cheap but still)