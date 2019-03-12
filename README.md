#  Fingerprint tool for CAD Model-based object detection

This project is part of Olin College's Spatial Computing Lab.


With this tool, we hope to develop and prove various fingerprintning algorithms to quickly and efficiently identify a CAD model from a live video feed.

This project focuses on the development of the fingerprintning algorithm with the goal to produce a model to be used in the live feed.


To be used as:
    python test-fingerprint.py <finger_print_model> <cad_model>

<cad_model> will default to the default model in the test/models/ folder


### Project Roadmap

#### Part 1
- [x] Load any STEP file into a usable format with Python
- [ ] Load any STEP file into a usable format via command line
- [ ] Automatically load STEP file from Onshape's API
- [ ] Generate CAD model contour at any angle
- [ ] Generate CAD model contour and internal features with occlusion

#### Part 2
- [ ] Load a fingerprintning algorithm with code
- [ ] Load a fingerprintning algorithm with command line
- [ ] Load a fingerprintning algorithm with web browser
- [ ] Load any STEP file into a usable format with a web browser
- [ ] Develop tools to compare fingerprintning algorithm
- [ ] Automate testing and refinement of different fingerprintning algorithms
