#import "@local/note_taking:1.0.0": conf

#show: doc => conf(
  title: [Geometric Median],
  author: [Gerardo Lujan Hernandez],
  doc,
)

= Notes

== Definition
For a given set of _m_ points $XX^m = x_1,x_2,...,x_m$ with each $x_i in RR^n$, the geometric median is defined as the minimizer of the sum of the $L_2$ distances:

$"argmin"_{y in RR^n} sum_{i=1}^m w_i||x_i - y||_2$ where "argmin" means the value of the argument y which minimizes the sum and $w_i$ represents a functional weight corresponding to the importance of the point. In this case, it is the point $y$ in n-dimensional Euclidean space from where the sum of all Euclidean distances to the $x_i$'s is minimum.

== Properties
- For the 1-dimensional case, the geometric median coincides with the median. This is because the univariate median also minimizes the sum of distances from the points
  - More precisely, if the points are $p_1,..,p_n$ in that order, the geometric median is the middle point $p_{(n+1)/2}$ if $n$ is odd, but is not uniquely determined if $n$ is even, when it can be any point in the line segment between the two middling points $p_{n/2}$ and $p_{(n/2)+1}$
- The geometric median is unique whenever the points are not collinear
- The geometric median is equivalent for Euclidean similarity transformations, including translation and rotation
  - This means that one would get the same result either by transforming the geometric median, or by applying the same transformation to the sample data and finding the geometric median from the transformed data

== Computation
A common approach to this problem is the *Weiszfeld's Algorithm* which is a form of #link("https://en.wikipedia.org/wiki/Iteratively_re-weighted_least_squares")[iteratively re-weighted least squares]. This algorithm defines a set of weights that are inversely proportional to the distances from the current estimate to the sample points, and creates a new estimate that is the weighted average of the sample according to these weights (these are weights specific to the iteration itself). That is,
$y_{k+1} = (sum^m_{i=1} frac(x_1, {||x_i - y_k||})) \/ (sum_{i=1}^m frac(1, {||x_i - y_k||}))$. This method may fail to converge with one of its estimates falls on one of the given points.


