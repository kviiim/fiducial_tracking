# Fiducial Tracking: Line Segmentation
by Annabelle Platt and Kate Mackowiak 

## Project Goals
The original goal of our project of our project was to recreate the fiducial tracking methods in [this paper](https://april.eecs.umich.edu/media/pdfs/olson2011tags.pdf) by Edwin Olson (2011). In the paper, Olson discusses the development of an (at the time) new type of fiducial tag known as April Tags. While similar to QR codes, these tags have several advantages. They are much smaller, and able to be used in applications where the lighting might not be ideal. These have now become widely used in robotics. Olson describes the algorithms his team used to detect tags using line segmentation. 

Originally we aimed to recreate the entire algorithm from scratch and be able to successfully identify an April Tag. While libraries exist that can get a roboticist up and running with April Tag identification in an hour or two, our learning goals were to understand what these kinds of libraries were doing under the hood. How can you take a raw image from a camera feed and process it to the point where you can identify an April tag within it, despite uneven lighting, scaling, and rotation? However, this turned out to be overly ambitious. While we read the whole paper, and understood it on a conceptual level, due to to time constraints we settled for reimplementing the first section only, which was line segmentation.

## Method
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

We then sort those edges by weight in ascending order, such that the two pixels with the closest gradient direction are at index 0. This enables us to loop through each edge in the graph, and decide if the two nodes have similar enough gradients to be considered as part of a segment. 

To determine if two gradients are similar enough to combine, we evaluate the following expressions:

$ D(n\bigcup m) \leq min(D(n),D(m)) + K_D / |n\bigcup m|$
$ M(n\bigcup m) \leq min(M(n),M(m)) + K_M / |n\bigcup m|$

Here, D(n) is the range of gradient directions in a segment, and M(n) is the range of gradient magnitudes in the segment. For one pixel this will just be the direction and magnitude of the pixel's gradient, but for a larger cluster this would be the maximum pixel direction minus the minimum pixel direction, and likewise the maximum pixel magnitude minus the minimum pixel magnitude.

K_D and K_M are parameters that allow for tuning. We use 100 and 1200 respectively, as that is what the paper stated worked best for them. 

We then create a set of nodes to store that segment. We repeat this process, however if a node is already in a set, we then take the union of each node's existing set to combine them. 

At the end of this process, we have a list of sets, each representing a different segment of the image. 

## Design Decisions 
One design decision that we made was in how we calculated the gradient. There are many different methods that we could have used. We chose to look at the pixels directly before and after the current pixel - effectively a 3x3 kernel. This means that we get a better overall picture of the change occurring. However, since we're not looking directly at a pixel but rather to the right and left, in very small images it can mean that we don't catch sudden changes between light and dark. 

This choice necessitated that we find a different method of calculating the gradient at the edges of the image. We ended up deciding to just compare the current pixel value to the one before or after (depending on which edge we were looking at). We noticed that not calculating the gradient at the edges of the image resulted in our segmentation algorithm finding "fake" segments at the image borders, but made the decision that in a realistic scenario where we are looking for a fiducial tag, the edges of the image are not super important as we will likely not be able to find a cut off tag anyways so this shortcut was fine for our application.

## Challenges 
One challenge that we faced was in designing our code to run in a reasonable time. In part, this is a result of using python for our implementation, but also had to do with how we structured our code. We faced a lot of tradeoffs in writing clean, easy to read code, and code which runs efficiently. As our learning goals in this project were to learn about the algorithm we were studying, we chose to start by implementing it in a way which made it easy for us to understand what we were doing. However this resulted in long testing times for images of any significant size. 

## Improvements 
We know that the image segmentation is the most computationally intensive part. Currently it runs in seconds on a 10x10 image, but takes at least 8 minutes on a 600x400 image which is much more similar to something you would get from a camera feed. Given more time we would have liked to rewrite our segmentation code to make it more efficient. We determine that to do this we would need to rewrite our data structures, so we opted not to do this in this iteration. 

We also would have loved to start identifying which line segments were connected to each other and finding quads (which are simply four-sided shapes). We were confused because the paper stated that they used a depth-first search technique (finding all side for one quad before moving on to the next) rather than a breadth-first search technique (finding all the line segments that could be joined at right angles, then finding a third segment for each, then finding the last segment), which we felt would have made more sense in this context. This would have been interesting to experiment with. 

## Takeaways 
One of our main takeaways was that project scoping is difficult, and even when you have a resource that you are recreating the implementation may take longer than anticipated. In future, we will budget more time to implementation as that required more time than we initially predicted.