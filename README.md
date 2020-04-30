# NonParametricDensityEstimation
This project based on section 6.1 is applying the Kernel Density Estimation method which
is a non-parametric way to estimate the probability density function of a random variable
on planetary-related data. This method provides a new direction for studying the M–R
relation when more mass and radius measurements are obtained with future missions
like TESS and PLATO.
In this project, I used this technique for estimating the density of exoplanets based on MR
relation. I imported the dataset from http://exoplanets.org/table. They are around 3000
datapoints of exoplanets and their characteristics. First, estimated the mean M-R
Relation. From the plot, there are three contiguous regions between which the M–R
relation changes: 0.0 R⊕ < r < 5 R⊕, 5 R⊕ < r < 11 R⊕, and <11 R⊕.
Then, applied the Gaussian Kernel density estimation for 2000 random sample of
exoplanet’s masses (planetary masses) by sampling them based on each sample’s radii.
Plotting them as histogram and pdf. From the histogram, the major peak is showed in
region from 0.0 to 1.5, and from 2.3 to 2.45. In this case, the PDF is a good fit for the
histogram. It is not very smooth and could be made more so by setting the “bandwidth”
argument to (0.02).
