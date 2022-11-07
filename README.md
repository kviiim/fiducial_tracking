# Fiducial Tracking: Line Segmentation
by Annabelle Platt and Kate Mackowiak 

## Project Goals
The original goal of our project of our project was to recreate the fiducial tracking methods in [this paper](https://april.eecs.umich.edu/media/pdfs/olson2011tags.pdf) by Edwin Olson (2011). In the paper, Olson discusses the development of an (at the time) new type of fiducial tag known as April Tags. While similar to QR codes, these tags have several advantages. They are much smaller, and able to be used in applications where the lighting might not be ideal. These have now become widely used in robotics. Olson describes the algorithms his team used to detect tags using line segmentation. 

Our original goal was to recreate the entire algorithm from scratch and be able to successfully identify an April Tag. While libraries exist that can get a roboticist up and running with April Tag identification in an hour or two, our learning goals were to understand what these kinds of libraries were doing under the hood. How can you take a raw image from a camera feed and process it to the point where you can identify an April tag within it, despite uneven lighting, scaling, and rotation? However, this turned out to be overly ambitious. While we read the whole paper, and understood it on a conceptual level, due to to time constraints we settled for reimplementing the first section only, which was line segmentation.

## Method
How did you solve the problem (i.e., what methods / algorithms did you use and how do they work)? As above, since not everyone will be familiar with the algorithms you have chosen, you will need to spend some time explaining what you did and how everything works.

At its essence, segmentation is finding groups of pixels that are connected to each other. 

## Design Decisions 
Describe a design decision you had to make when working on your project and what you ultimately did (and why)? These design decisions could be particular choices for how you implemented some part of an algorithm or perhaps a decision regarding which of two external packages to use in your project.

## Challenges 
What if any challenges did you face along the way?

## Improvements 
What would you do to improve your project if you had more time?

## Takeaways 
Did you learn any interesting lessons for future robotic programming projects? These could relate to working on robotics projects in teams, working on more open-ended (and longer term) problems, or any other relevant topic.