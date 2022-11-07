# Fiducial Tracking: Line Segmentation
by Annabelle Platt and Kate Mackowiak 

## Project Goals
The original goal of our project of our project was to recreate the fiducial tracking methods in [this paper](https://april.eecs.umich.edu/media/pdfs/olson2011tags.pdf) by Edwin Olson (2011). In the paper, Olson discusses the development of an (at the time) new type of fiducial tag known as April Tags. While similar to QR codes, these tags have several advantages. They are much smaller, and able to be used in applications where the lighting might not be ideal. These have now become widely used in robotics. Olson describes the algorithms his team used to detect tags using line segmentation. 

Our original goal was to recreate the entire algorithm from scratch and be able to successfully identify an April Tag. While libraries exist that can get a roboticist up and running with April Tag identification in an hour or two, our learning goals were to understand what these kinds of libraries were doing under the hood. How can you take a raw image from a camera feed and process it to the point where you can identify an April tag within it, despite uneven lighting, scaling, and rotation? However, this turned out to be overly ambitious. While we read the whole paper, and understood it on a conceptual level, due to to time constraints we settled for reimplementing the first section only, which was line segmentation.

## Method
How did you solve the problem (i.e., what methods / algorithms did you use and how do they work)? As above, since not everyone will be familiar with the algorithms you have chosen, you will need to spend some time explaining what you did and how everything works.

### Image Segementation Overview
At its essence, segmentation is finding groups of pixels that are connected to each other. In fiducial tags, we know that the tag itself is black and white, so the idea  is to connect black pixels to black pixels and white pixels to white pixels if they appear close enough to each other. By "close" we mean close enough in two metrics: gradient magnitude and gradient direction. 

### Gradients 
The gradient is how much pixels change in a given direction (see [this Wikipedia page](https://en.wikipedia.org/wiki/Image_gradient) for more details about gradients). We calculated the gradient for the image in the x direction from left to right, and the y direction from top to bottom. 

The gradient magnitude is simply how large the gradient is - in other words, how much the pixels change. This can be calculated with a standard magnitude calculation: 

$mag = \sqrt{x^2 + y^2}$

where x and y are the gradient in the x and y direction. 

The gradient direction is the angle at which the gradient changes, and can be calculated by taking the inverse tangent of the y gradient over the x gradient: 

$ \arctan{\frac{y}{x}}$

### Clustering
Once the magnitude and direction had been calculated for each pixel, we create a graph with edges between pixels that are physically adjecent in the image. The edge weight is equal to the difference between the two pixels' gradient directions. 

## Design Decisions 
Describe a design decision you had to make when working on your project and what you ultimately did (and why)? These design decisions could be particular choices for how you implemented some part of an algorithm or perhaps a decision regarding which of two external packages to use in your project.

- make image greyscale 
- calculate gradient not looking directly at pixel
- gradient calculation around the edges 

## Challenges 
What if any challenges did you face along the way?

## Improvements 
What would you do to improve your project if you had more time?

We know that the image segmentation is the most computationally intensive part. Currently it runs in seconds on a 10x10 image, but takes at least 8 minutes on a 600x400 image which is much more similar to something you would get from a camera feed. Given more time we would have liked to rewrite our segmentation code to make it more efficient. We determine that to do this we would need to rewrite our data structures, so we opted not to do this in this iteration. 

We also would have loved to start identifying which line segments were connected to each other and finding quads (which are simply four-sided shapes). We were confused because the paper stated that they used a depth-first search technique (finding all side for one quad before moving on to the next) rather than a breadth-first search technique (finding all the line segments that could be joined at right angles, then finding a third segment for each, then finding the last segment), which we felt would have made more sense in this context. This would have been interesting to experiment with. 

## Takeaways 
Did you learn any interesting lessons for future robotic programming projects? These could relate to working on robotics projects in teams, working on more open-ended (and longer term) problems, or any other relevant topic.